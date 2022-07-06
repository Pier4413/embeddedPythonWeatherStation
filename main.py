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


class MainApp:

    def __init__(self) -> None:
        self.start_app()

        self.weather_queue = Queue(100)  # The weather queue
        self.weather_worker = WeatherWorker(
            delay_time=Settings.get_instance().getint("general", "delay", 60),
            weather_queue=self.weather_queue,
            is_simulated=Settings.get_instance().getboolean("general", "is_simulated", False)
        )  # The weather worker
        self.has_to_read_weather_external = True  # The
        self.reading_thread = None
        self.data_request = DataRequest(os.environ["API_KEY"])

        self.start_threads()

    def start_threads(self):
        self.weather_worker.start()

    def clean_up(self, signal_received, frame):
        """
            Cleaning function at application death
        """

        if(self.weather_worker is not None):
            self.weather_worker.has_to_read_weather = False
            self.weather_worker.join(timeout=5)

        self.has_to_read_weather_external = False
        
        e = None
        while e == None:
            Logger.get_instance().debug(f"Emptying queue")
            try:
                self.weather_queue.get()
            except Empty as empty:
                e = empty    
            finally:    
                self.weather_queue.task_done()

        Logger.get_instance().info(f"Quitting the application with status 0")
        sys.exit(0)

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

        # Attach signals
        signal.signal(signal.SIGABRT, self.clean_up)
        signal.signal(signal.SIGILL, self.clean_up)
        signal.signal(signal.SIGINT, self.clean_up)
        signal.signal(signal.SIGSEGV, self.clean_up)
        signal.signal(signal.SIGTERM, self.clean_up)

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
        if(self.weather_queue.empty() is not True):
            item = self.weather_queue.get()
            try:
                self.progress_weather_worker(item)
            except Empty:
                Logger.get_instance().debug(f"Empty queue doing nothing")
            except Exception as e:
                Logger.get_instance().error(f'error while processing item {e}')
            finally:
                self.weather_queue.task_done()

    def read_weather(self):
        while self.has_to_read_weather_external:
            self.read_queue()
            sleep(1)


if __name__ == "__main__":
    mainApp = MainApp()
    mainApp.read_weather()
