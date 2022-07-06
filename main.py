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

        if(mainApp.thread_read is not None):
            mainApp.thread_read.join(timeout=5)

        if(mainApp.weather_worker is not None):
            mainApp.weather_worker.has_to_read_weather = False
            mainApp.weather_worker.join(timeout=5)

        Logger.get_instance().info(f"Quitting the application with status {signal_received}")
        os.kill(os.getpid(), 0)

class MainApp:

    def __init__(self, async_read: bool = True) -> None:
        self.start_app()

        self.weather_queue = Queue(100)  # The weather queue
        self.weather_worker = WeatherWorker(
            delay_time=Settings.get_instance().getint("general", "delay", 60),
            weather_queue=self.weather_queue,
            is_simulated=Settings.get_instance().getboolean("general", "is_simulated", False),
            rotation_radius=Settings.get_instance().getfloat("anemometer", "sensor_radius", 0.1)
        )  # The weather worker
        self.has_to_read_weather_external = True
        self.data_request = DataRequest(os.environ["API_KEY"])

        self.thread_read = None
        if(async_read is True):
            self.thread_read = self.create_async_read()

        self.start_threads()

    def start_threads(self):
        if(self.weather_worker is not None):
            self.weather_worker.start()
        else:
            Logger.get_instance().error(f"Can't start the weather worker is None")

        if(self.thread_read is not None):
            self.thread_read.start()

    

    def start_app(self):
        # Default values for options
        confFileName = "./conf/settings.ini"
        envFileName = "./conf/.env"
        logInfo = "./logs/info.log"
        logCritical = "./logs/critical.log"
        logLevel = 20

        # Process command line options
        try:
            opts, args = getopt.getopt(sys.argv[1:], "", [
                                       "settings=", "env=", "log_level=", "log_info_file=", "log_crit_file="])
        except Exception as e:
            print(f"{e}")
            self.clean_up(0, 0)

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
            else:
                print(f"Option not handled {opt}")

        # Logger loading
        Logger.get_instance().load_logger(info_file=logInfo,
                                          critical_file=logCritical, console=True, level=logLevel)

        # Dot env file
        load_dotenv(envFileName)

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

    def create_async_read(self):
        return threading.Thread(target=self.read_weather)
        

if __name__ == "__main__":
    
    # Attach signals
    signal.signal(signal.SIGABRT, clean_up)
    signal.signal(signal.SIGILL, clean_up)
    signal.signal(signal.SIGINT, clean_up)
    signal.signal(signal.SIGSEGV, clean_up)
    signal.signal(signal.SIGTERM, clean_up)
    #signal.signal(2, clean_up)

    mainApp = MainApp(async_read=False)
    mainApp.read_weather()
    
