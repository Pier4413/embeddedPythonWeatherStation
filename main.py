from queue import (Queue, Empty)
import signal
import sys
import getopt
import threading
import os

from dotenv import (
    load_dotenv
)

from time import sleep

from classes.element.weather import Weather
from classes.http_request.data_request import DataRequest
from workers.weather_worker import WeatherWorker
from modules.logger.logger import Logger
from modules.settings.settings import Settings

mainApp = None

def clean_up(signal_received, frame):
    """
        Cleaning function at application death
    """
    if(mainApp is not None):
        Logger.get_instance().info(f"Starting to stop the application signal {signal_received} received")

        mainApp.has_to_read_weather_external = False

        if(mainApp.weather_worker is not None):
            mainApp.weather_worker.has_to_read_weather = False
            mainApp.weather_worker.join(timeout=5)

        Logger.get_instance().info(f"Quitting the application with status 0")
        os.kill(os.getpid(), 0)

class MainApp:

    def __init__(self) -> None:
        
        self.has_to_read_weather_external = True
        
        self.start_app()

        self.weather_queue = Queue(100)  # The weather queue
        self.weather_worker = WeatherWorker(
            weather_queue=self.weather_queue
        )  # The weather worker
        self.data_request = DataRequest(os.environ["API_KEY"])

        self.start_threads()

    def start_threads(self):
        if(self.weather_worker is not None and self.has_to_read_weather_external is True):
            self.weather_worker.start()
        else:
            Logger.get_instance().error(f"Can't start the weather worker is None")
   
    def print_help(self):
        self.has_to_read_weather_external = False
        print("- --help : print the help\n"+
            "- --settings : providing the path of the ini config file (default : ./conf/settings.ini)\n"+
            "- --env : providing the path of a .env file (default : ./conf/.env)\n"+
            "- --log_level : The log level. A lower level include the higher ones\n"+
            "\t- DEBUG : 10\n"+
            "\t- INFO : 20\n"+
            "\t- WARN : 30\n"+
            "\t- ERROR : 40\n"+
            "- --log_info_file : To log all infos (default : None)\n"+
            "- --log_crit_file : To log error infos (default : None)\n"+
            "- --log_console : To log all infos in the console (default : 0)\n")
        clean_up(0, 0)

    def check_environ(self, *args):
        for k in args:
            if(os.getenv(k) is None):
                Logger.get_instance().error(f"{k} environment variable doesn't exists please provide it or see ReadMe")
                clean_up(0, 0)

    def start_app(self):

        # Default values for options
        confFileName = "./conf/settings.ini"
        envFileName = "./conf/.env"
        logInfo = None
        logCritical = None
        logConsole = False
        logLevel = 20

        # Process command line options
        try:
            opts, args = getopt.getopt(sys.argv[1:], "", ["settings=", "env=", "log_level=", "log_info_file=", "log_crit_file=", "log_console=", "help"])
        except Exception as e:
            print(f"{e}")
            clean_up(0, 0)

        for opt, arg in opts:
            if opt in ['-s', "--settings"]:
                confFileName = arg
            elif opt in ['-e', "--env"]:
                envFileName = arg
            elif opt in ["--log_level"]:
                logLevel = int(arg)
            elif opt in ["--log_info_file"]:
                logInfo = arg
            elif opt in ["--log_crit_file"]:
                logCritical = arg
            elif opt in ["--log_console"]:
                logConsole = arg
            elif opt in ["--help"]:
                self.print_help()
            else:
                print(f"Option not handled {opt}")

        # Logger loading
        Logger.get_instance().load_logger(app_name="Weather station", info_file=logInfo,
                                          critical_file=logCritical, console=logConsole, level=logLevel)

        # Dot env file
        load_dotenv(envFileName)
        
        self.check_environ()

        # Printing options for debug purposes in the logger (i.e in files and console if wanted)
        Logger.get_instance().info(f"Given options : ")
        Logger.get_instance().info(f"--settings={confFileName}")
        Logger.get_instance().info(f"--env={envFileName}")
        Logger.get_instance().info(f"--log_level={logLevel}")
        Logger.get_instance().info(f"--log_info_file={logInfo}")
        Logger.get_instance().info(f"--log_crit_file={logCritical}")

        # Load settings
        Settings.get_instance().load_settings(confFileName)

    def progress_weather_worker(self, weather: Weather) -> None:
        """
            Function to be executed when the progress signal of weather worker is sent

            :param weather: The new weather
            :type weather: Weather
        """
        if weather == None:
            Logger.get_instance().error("No weather provided")
        else:
            # Print the weather to debug for information
            Logger.get_instance().debug(weather)

            try:
                response = self.data_request.makeRequest(
                    uri=os.environ["API_SERVER_URL"],
                    url="weather",
                    params=weather.__dict__(),
                    methodHTTP="POST"
                )
                Logger.get_instance().info(
                    f"The data has been saved {response}")
            except Exception as e:
                Logger.get_instance().error(
                    f"Data not saved an exception occured {e}")

    def read_queue(self):
        if(self.has_to_read_weather_external is True):
            item = None
            try:
                item = self.weather_queue.get(block=False, timeout=5)
                self.weather_queue.task_done()
            except Empty:
                Logger.get_instance().debug(f"Empty queue doing nothing")
            except Exception as e:
                Logger.get_instance().error(f'error while processing item {e}')
            self.progress_weather_worker(item)

    def read_weather(self):
        while True:
            if(self.has_to_read_weather_external is False):
                Logger.get_instance().info(f"Killing the queue reading thread")
                break
            self.read_queue()
            sleep(10)
       

if __name__ == "__main__":
    
    # Attach signals
    signal.signal(signal.SIGABRT, clean_up)
    signal.signal(signal.SIGILL, clean_up)
    signal.signal(signal.SIGINT, clean_up)
    signal.signal(signal.SIGSEGV, clean_up)
    signal.signal(signal.SIGTERM, clean_up)
    #signal.signal(2, clean_up)

    mainApp = MainApp()
    mainApp.read_weather()
    
