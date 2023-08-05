import sys, os
import argparse
import logging
import shutil
from . import util 
from .orchestrator import Orchestration
from . import admin
import pandas as pd

l = logging.getLogger("pandem")

def main(a):
  #conf = config()
  # Base argument parser
  parser = argparse.ArgumentParser()
  subs = parser.add_subparsers()
  
  # Launch pandem source start command
  start_parser = subs.add_parser("start", help = "Starts PANDEM source monitor")
  
  start_parser.add_argument(
    "-d", 
    "--debug", 
    action="store_true", 
    help="Whether to output debugging messages to the console", 
  )
  
  start_parser.add_argument(
    "--no-acquire", 
    action="store_true", 
    help="Prevent data acquisition from sources", 
  )
  
  start_parser.add_argument(
    "--no-nlp", 
    action="store_true", 
    help="Prevent NLP models and sources using them (Twitter, MediSys) pf being launched (Useful for instances without docker" 
  )

  start_parser.add_argument(
    "--retry-failed", 
    action="store_true", 
    help="Whether to retry failed jobs" 
  )
  
  start_parser.add_argument(
    "--not-retry-active", 
    action="store_true", 
    help="Whether to do not retry active jobs" 
  )
  start_parser.add_argument(
    "--no-app", 
    action="store_true", 
    help="If present the pandem2-source app will not be lauched" 
  )
  start_parser.add_argument(
    "--force-acquire", 
    action="store_true", 
    help="Reset the concerned data sources to force a fresh acquire" 
  )

  start_parser.add_argument(
    "-r",
    "--restart-job", 
    type=int, 
    required = False,
    default = 0,
    help="Job id to re-run if its data is still stored" 
  )
  
  start_parser.add_argument(
    "-l",
    "--limit-collection", 
    help="Comma separated list of sources for limiting the collection" 
  )
  
  start_parser.set_defaults(func = do_start)
  
  # setup 
  reset_parser = subs.add_parser("reset", help = "reset configuration as system defaults")
  
  reset_parser.add_argument(
    "-v", 
    "--variables", 
    action="store_true", 
    help="Whether to restore variables defiitions to last system defaults", 
  )
  reset_parser.add_argument(
    "--restore-factory-defaults", 
    action="store_true", 
    help="Delete all files and database elements and restore system defaults", 
  )
  reset_parser.add_argument(
    "--scripts",
    action="store_true",
    help="Restore the default script folder in pandem-home"
  )
  reset_parser.add_argument(
    "--covid19-datahub", 
    action="store_true", 
    help="Reset covid19-datahub datasource to system defaults", 
  )
  reset_parser.add_argument(
    "--ecdc-atlas", 
    action="store_true", 
    help="Reset ecdc-atlas datasource to system defaults", 
  )
  reset_parser.add_argument(
    "--influenzanet", 
    action="store_true", 
    help="Reset influenza net datasource to system defaults", 
  )
  reset_parser.add_argument(
    "--ecdc-covid19", 
    action="store_true", 
    help="Reset ecdc-covid19 datasource to system defaults", 
  )
  reset_parser.add_argument(
    "--ecdc-covid19-simulated", 
    action="store_true", 
    help="Reset ecdc-covid19 simulated datasource to system defaults", 
  )
  reset_parser.add_argument(
    "--serotracker", 
    action="store_true", 
    help="Reset serotracker datasource to system defaults", 
  )
  reset_parser.add_argument(
    "--pandem-partners-template", 
    action="store_true", 
    help="Reset pandem partner templates to system defaults", 
  )
  reset_parser.add_argument(
    "--twitter", 
    action="store_true", 
    help="Reset pandem twitter system defaults", 
  )
  reset_parser.add_argument(
    "--medisys", 
    action="store_true", 
    help="Reset pandem medisys system defaults", 
  )
  reset_parser.add_argument(
    "--flights",
    action="store_true",
    help="Reset pandem flight related information to system defaults", 
  )
  reset_parser.add_argument(
    "--owid",
    action="store_true",
    help="Reset pandem owid related information to system defaults"
  )

  reset_parser.set_defaults(func = do_reset)

  # Launch pandem source listt command
  start_parser = subs.add_parser("list", help = "List elements on this Pandem-Source instance")
  start_parser.add_argument(
    "--sources",
    action="store_true",
    help="List existing sources in this instance", 
  )
  
  start_parser.add_argument(
    "--missing-sources",
    action="store_true",
    help="List sources embedded on pandemSource package not present on this instance", 
  )
  start_parser.add_argument(
    "--package-sources",
    action="store_true",
    help="List sources embedded on pandemSource package", 
  )
  start_parser.add_argument(
    "--missing-package-sources",
    action="store_true",
    help="List existing sources in this instance not present on pandemSource package", 
  )

  start_parser.set_defaults(func = do_list)

  
  util.check_pandem_home()
  #calling handlers
  func = None
  try:
    args = parser.parse_args()
    func = args.func
  except AttributeError:
    parser.print_help()
  if func != None:
    args.func(args, parser)

# handlers
def do_start_dev(debug = True, no_acquire = False, retry_failed = False, restart_job = 0, not_retry_active = False, no_app = True, force_acquire = False, no_nlp = False):
  from types import SimpleNamespace
  return do_start(SimpleNamespace(**{"debug":True, "no_acquire":no_acquire, "retry_failed":retry_failed, "limit_collection":None, "restart_job":restart_job, "no_app":no_app, "not_retry_active":not_retry_active, "force_acquire":force_acquire, "no_nlp": no_nlp}))

# handlers
def do_start(args, *other):
  if args.debug:
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
 
  pkg_dir, this_filename = os.path.split(__file__)
  defaults = os.path.join(pkg_dir, "data/defaults.yml") 
  config = util.pandem_path("settings.yml")
  if not os.path.exists(config):
    shutil.copy(defaults, config)

  # Adding python scripts on pandem_home to the system path
  sys.path.insert(1, util.pandem_path("files", "scripts", "py"))
  settings = util.settings()
  
  install_issues = admin.install_issues(check_nlp = not args.no_nlp)
  if len(install_issues) > 0:
    eol = '\n'
    l.warning(f"""The following errors where found on current PANDEM-2 installation please fix before proceed
    {eol.join(install_issues)}
    """)
    return None
  
  if args.restart_job > 0:
    orchestrator_ref = Orchestration.start(
      settings, 
      start_acquisition = False, 
      retry_failed = False, 
      restart_job = args.restart_job, 
      retry_active = True, 
      force_acquire = args.force_acquire, 
      no_nlp = args.no_nlp
    )
    orch = orchestrator_ref.proxy()
  elif args.limit_collection is not None:
    orchestrator_ref = Orchestration.start(
      settings, start_acquisition = False, 
      retry_failed = args.retry_failed, 
      restart_job = args.restart_job, 
      retry_active = 
      not args.not_retry_active, 
      force_acquire = args.force_acquire, 
      no_nlp = args.no_nlp
    )
    orch = orchestrator_ref.proxy()
    storage_proxy = orch.get_actor("storage").get().proxy()
    dls_files = storage_proxy.list_files('source-definitions').get()
    dls_dicts = [storage_proxy.read_file(file_name['path']).get() for file_name in dls_files if file_name['path'].endswith(".json")]
    for source_name in args.limit_collection.split(","):
      dlss = list(filter(lambda dls: dls['scope']['source'] == source_name or (source_name in dls['scope']['tags'] and (dls['acquisition'].get("active") != False)), dls_dicts))
      for dls in dlss:
        acquisition_proxy = orch.get_actor(f"acquisition_{dls['acquisition']['channel']['name']}").get().proxy()
        acquisition_proxy.add_datasource(dls, args.force_acquire)
  else:
    orchestrator_ref = Orchestration.start(
      settings, 
      start_acquisition = not args.no_acquire, 
      retry_failed = args.retry_failed, 
      retry_active = not args.not_retry_active, 
      force_acquire = args.force_acquire, 
      no_nlp = args.no_nlp
    )
    orch = orchestrator_ref.proxy()

  # launching pandem2source app
  if not args.no_app:
    admin.run_pandem2app()    

  return orch
  
def do_reset(args, *other):
  if args.restore_factory_defaults:
    admin.delete_all()
    admin.reset_default_folders("input-local", "input-local-defaults", "dfcustom", "scripts", "variables", "indicators", "img")
  if args.scripts:
    admin.reset_default_folders("scripts")
  if args.variables or args.restore_factory_defaults:
    admin.reset_variables()
  if args.covid19_datahub or args.ecdc_covid19 or args.restore_factory_defaults:
    admin.reset_source("nuts-eurostat")
    admin.reset_source("ICD-10-diseases-list")
  if args.pandem_partners_template or args.restore_factory_defaults:
    admin.reset_source("covid19-template-cases")
    admin.reset_source("covid19-template-cases-RIVM")
    admin.reset_source("covid19-template-cases-THL")
    admin.reset_source("covid19-template-beds-staff")
    admin.reset_source("covid19-template-contact-tracing")
    admin.reset_source("covid19-template-daily-voc-voi")
    admin.reset_source("covid19-template-daily-voc-voi-RIVM")
    admin.reset_source("covid19-template-hospitalised-deaths")
    admin.reset_source("covid19-template-hospitalised-deaths-THL")
    admin.reset_source("covid19-template-hospitalised-deaths-RIVM")
    admin.reset_source("covid19-template-ltcf-RIVM")
    admin.reset_source("covid19-template-outbreaks")
    admin.reset_source("covid19-template-participatory-sentinel-surveilla")
    admin.reset_source("covid19-template-sex-age-comorbidity")
    admin.reset_source("covid19-template-testing")
    admin.reset_source("covid19-template-testing-THL")
    admin.reset_source("covid19-template-testing-RIVM")
    admin.reset_source("covid19-template-vaccination")
    admin.reset_source("covid19-template-vaccination-THL")
    admin.reset_source("covid19-template-voc-voi")
    admin.reset_source("covid19-template-local-regions")
    admin.reset_source("covid19-template-local-regions-RIVM")
    admin.reset_source("covid19-template-local-regions-THL")
  if args.covid19_datahub or args.restore_factory_defaults:
    admin.reset_source("covid19-datahub")
    admin.reset_source("covid19-datahub-AUT")
    admin.reset_source("covid19-datahub-BEL")
    admin.reset_source("covid19-datahub-BGR")
    admin.reset_source("covid19-datahub-HRV")
    admin.reset_source("covid19-datahub-CYP")
    admin.reset_source("covid19-datahub-CZE")
    admin.reset_source("covid19-datahub-DNK")
    admin.reset_source("covid19-datahub-EST")
    admin.reset_source("covid19-datahub-FIN")
    admin.reset_source("covid19-datahub-FRA")
    admin.reset_source("covid19-datahub-DEU")
    admin.reset_source("covid19-datahub-GRC")
    admin.reset_source("covid19-datahub-HUN")
    admin.reset_source("covid19-datahub-IRL")
    admin.reset_source("covid19-datahub-ITA")
    admin.reset_source("covid19-datahub-LVA")
    admin.reset_source("covid19-datahub-LTU")
    admin.reset_source("covid19-datahub-LUX")
    admin.reset_source("covid19-datahub-MLT")
    admin.reset_source("covid19-datahub-NLD")
    admin.reset_source("covid19-datahub-POL")
    admin.reset_source("covid19-datahub-PRT")
    admin.reset_source("covid19-datahub-ROU")
    admin.reset_source("covid19-datahub-SVK")
    admin.reset_source("covid19-datahub-SVN")
    admin.reset_source("covid19-datahub-ESP")
    admin.reset_source("covid19-datahub-SWE")
    admin.reset_source("covid19-datahub-GBR")

  if args.ecdc_covid19_simulated or args.restore_factory_defaults:
    admin.reset_source("ecdc-covid19-age-group-variants")
    admin.reset_source("ecdc-covid19-weekly-hospital-occupancy-variants")
    admin.reset_source("ecdc-covid19-genomic-data")
  if args.ecdc_covid19 or args.restore_factory_defaults:
    admin.reset_source("ecdc-covid19-vaccination")
    admin.reset_source("ecdc-covid19-variants")
    admin.reset_source("ecdc-covid19-age-group")
    admin.reset_source("ecdc-covid19-measures")
    admin.reset_source("ecdc-covid19-daily")
    admin.reset_source("ecdc-covid19-weekly-hospital-occupancy")
  if args.serotracker or args.restore_factory_defaults:
    admin.reset_source("geonames-countries")    
    admin.reset_source("serotracker")    
  if args.ecdc_atlas or args.restore_factory_defaults:
    admin.reset_source("ecdc-atlas-influenza")    
  if args.influenzanet or args.restore_factory_defaults:
    admin.reset_source("influenza-net")
    admin.reset_source("influenza-net-visits")
  if args.twitter or args.restore_factory_defaults:
    admin.reset_source("twitter")    
  if args.medisys or args.restore_factory_defaults:
    admin.reset_source("medisys")
  if args.flights or args.restore_factory_defaults:
    admin.reset_source("ourairports")
    admin.reset_source("opensky-network-coviddataset")
  if args.owid or args.restore_factory_defaults:
    admin.reset_source("owid-covid19-excess-mortality")

def do_list(args, *other):
  if args.sources or args.missing_sources or args.package_sources or args.missing_package_sources:
    sources = admin.list_sources(local = args.sources, default = args.package_sources, missing_local = args.missing_sources, missing_default = args.missing_package_sources)
    for line in pd.DataFrame(sources,columns=["Source", "Tag"]).to_string().split("\n"):
        print(line)



if __name__ == "__main__":
  main(sys.argv[1] if len(sys.argv)>1 else None)


