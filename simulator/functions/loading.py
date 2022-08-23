import getopt
import sys

from modules.logger.logger import Logger
from modules.settings.settings import Settings

def load_settings(file : str = None) -> None:
  Settings.get_instance().load_settings(settings_file=file)

def start() -> None:
  confFileName = "./conf/settings.ini"

  # Process command line options
  try:
      opts, args = getopt.getopt(sys.argv[1:], "", ["settings=", "env=", "log_level=", "log_info_file=", "log_crit_file=", "log_console=", "help"])
  except Exception as e:
      print(f"{e}")

  for opt, arg in opts:
    if opt in ['-s', "--settings"]:
      confFileName = arg
    else:
      print(f"Option not handled {opt}")

  # Logger loading
  Logger.get_instance().load_logger(app_name="Weather station simulator", console=True, level=10)

  # Printing options for debug purposes in the logger (i.e in files and console if wanted)
  Logger.get_instance().info(f"Given options : ")
  Logger.get_instance().info(f"--settings={confFileName}")

  # Load settings
  load_settings(confFileName)