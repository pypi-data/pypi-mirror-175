import time
from . import worker
from abc import ABC, abstractmethod, ABCMeta
import numpy as np
import copy
import json
from .util import JsonEncoder
import logging

l = logging.getLogger("pandem.aggregator")

class Aggregator(worker.Worker):
  __metaclass__ = ABCMeta  
  def __init__(self, name, orchestrator_ref, settings): 
      super().__init__(name = name, orchestrator_ref = orchestrator_ref, settings = settings)    

  def on_start(self):
      super().on_start()
      self._storage_proxy = self._orchestrator_proxy.get_actor('storage').get().proxy()
      self._pipeline_proxy = self._orchestrator_proxy.get_actor('pipeline').get().proxy() 
      self._variables_proxy = self._orchestrator_proxy.get_actor('variables').get().proxy()

  def aggregate(self, list_of_tuples, job):
    list_of_tuples = self.distribute_tuples_by_var(list_of_tuples, job["id"])

    variables = self._variables_proxy.get_variables().get()
    geos = {var["variable"] for var in variables.values() if var["type"] == "geo_referential"}
    geo_parents = {var["linked_attributes"][0]:var["variable"] for var in variables.values() if var["type"] == "referential_parent" and var["linked_attributes"] is not None and var["linked_attributes"][0] in geos}

    var_asc = {code:self.rel_ascendants(self.descendants(code, parent)) for code, parent in geo_parents.items()}
    nvars = len(list_of_tuples)
    ndone = 0
    for var, var_tuples in list_of_tuples.items():
      # getting vartuples value from cache
      var_tuples = var_tuples.value()
      cumm = {}
      untouched = []
      for t in [t for t in var_tuples['tuples'] if "attr" in t or "obs" in t]:
        aggr_func =  self.tuple_aggregate_function(t, variables)
        if aggr_func is None:
          untouched.append(t)
        else:
          for aggr_key, tt in self.pairs_to_aggregate(t, var_asc, variables):
            if not aggr_key in cumm:
              cumm[aggr_key] = tt
            else:
              var_name = list(t["obs"].keys())[0]
              cumm[aggr_key]["obs"][var_name] = aggr_func([cumm[aggr_key]["obs"][var_name], tt["obs"][var_name]])

      result = var_tuples.copy()
      result['tuples'] = untouched + [*cumm.values()]
      
      ret = self._storage_proxy.to_job_cache(job["id"], f"agg_{var}", result).get()
      ndone = ndone + 1
      self._pipeline_proxy.aggregate_end(tuples = ret, var = var, progress = ndone/nvars, job = job)

  def descendants(self, code, parent):
    codes = self._variables_proxy.get_referential(code).get()
    if codes is None:
      return None
    rel = {t['attr'][code]:t['attrs'][parent] if parent in t['attrs'] else None for t in codes}
    return self.rel_descendants(rel) 

  def rel_descendants(self, rel, desc = {}):
    if len(desc) == 0:
      desc = {c:{c} for c, p in rel.items()}
    added = True
    while added:
      added = False
      for e, dd in desc.items():
        for c, p in rel.items():
          if p in dd and c not in desc[e]:
            desc[e].add(c)
            added = True
    return desc

  def rel_ascendants(self, descendants):
    if descendants is None:
      return None
    asc = {}
    for code, descs in descendants.items():
      for desc in descs:
        if not desc in asc:
          asc[desc] = {code}
        else:
          asc[desc].add(code)
    return asc

  def aggregate_function(self, unit):
    if unit is None:
      return lambda values: None 

    unit = unit.lower().replace(" ", "")
    if unit in ['people', 'number', 'qty', 'days']:
        return np.sum
    elif unit in ['comma_list']:
      return ','.join
    else:
      return lambda values: None 
   

  def tuple_aggregate_function(self, t, variables):
    if ("obs" in t 
      and len(t["obs"].keys()) > 0 
      and list(t["obs"].keys())[0] in variables 
      and "unit" in variables[list(t["obs"].keys())[0]] ):
        return self.aggregate_function(variables[list(t["obs"].keys())[0]]["unit"])
    else:
        return None

  def pairs_to_aggregate(self, t, var_asc, variables):
    if not "attrs" in t or len(t["attrs"].keys()) == 0:
      yield ('', t)
    else:
      keys = [attr for attr in t["attrs"].keys() if variables[attr]["type"] in ["characteristic", "referential", "geo_referential", "date", "referential_parent"]]
      keys.sort()
      # adding identity aggregation 
      yield (json.dumps({list(t["obs"].keys())[0]:[(key,t["attrs"][key]) for key in keys]}, cls=JsonEncoder), t)

      # adding ascendants aggregation
      for code_var, ascendants in var_asc.items():
        if code_var in t["attrs"] and t["attrs"][code_var] in ascendants:
          code =  t["attrs"][code_var]
          for asc in ascendants[code]:
            c = copy.deepcopy(t)
            c["attrs"][code_var] = asc
            keys = [attr for attr in c["attrs"].keys() if variables[attr]["type"] in ["characteristic", "referential", "geo_referential", "date", "referential_parent"]]
            keys.sort()
            if(code != asc): # we have to remove the idenntity since it was already added
              yield (json.dumps({list(t["obs"].keys())[0]:[(key,c["attrs"][key]) for key in keys]}, cls=JsonEncoder), c)

  def distribute_tuples_by_var(self, tuples, job_id):
    tts = {}
    for p, tt in tuples.items():
      if tt is not None:
        # getting tuples from cache
        tt = tt.value()
        vars_in_path = set()
        for t in tt['tuples']:
          var = None
          for group in t.keys():
            if group !="attrs":
              var = next(iter(t[group].keys()))
          # initialization of the variables container (once per variable)
          if var not in tts and var is not None:
            tts[var] = {
              "tuples":[],
              "scope":{"update_scope":{}}
            }
          # If current variable is the first variable in path add all tuples of this variable
          if var not in vars_in_path:
            tts[var]['tuples'].extend(t for t in tt['tuples'] if var in t[group])
            vars_in_path.add(var)
            # updating the update scope 
            for u in tt['scope']['update_scope']:
              v = u["value"] if type(u["value"]) in [list, set] else [u["value"]]
              if u['variable'] in tts[var]['scope']['update_scope'] :
                 tts[var]['scope']['update_scope'][u['variable']].update(v)
              else:
                 tts[var]['scope']['update_scope'][u['variable']] = set(v)

    for var in tts.keys(): 
      tts[var]['scope']['update_scope'] = [{"variable":k, "value":list(v)} for k, v in tts[var]['scope']['update_scope'].items()]
      #storing results distributed by variables on cache
      tts[var] = self._storage_proxy.to_job_cache(job_id, f"agg_{var}", tts[var]).get()
    l.debug("Tuples redistributed by variables")
    return tts
