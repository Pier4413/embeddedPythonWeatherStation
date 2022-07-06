from math import pi
import os
from queue import Queue
from threading import Thread
from typing import Any
from time import sleep

from modules.logger.logger import Logger

from classes.element.position import Position
from classes.element.temperature import Temperature
from classes.element.wind import Wind
from classes.element.weather import Weather
from classes.element.miscellaneous import Miscellaneaous


class WeatherWorker(Thread):
    """
        Weather worker

        :author: Panda <panda@delmasweb.net>
        :date: January 15, 2022
        :version: 1.0
    """

    def __init__(self, delay_time: int = 60, weather_queue: Queue = None, is_simulated: bool = False, rotation_radius: float = 0.1) -> None:
        """
            Constructor

            :param delay_time: The time between two reads in seconds
            :type delay_time: int
            :param weather_queue: The queue in which we put the data
            :type weather_queue: Queue
            :param is_simulated: To allow use to simulated data without the sensors
            :type is_simulated: bool
        """
        super().__init__()
        self.delay_time = delay_time
        self.has_to_read_weather = True
        self.weather_queue = weather_queue
        self.is_simulated = is_simulated
        self.rotation_radius = rotation_radius

    def read_pressure_temperature_humidity(self, wind_speed):
        """
            Read data from the sensor (Pressure, Temperature and Humidity) from BME280
        """
        if(self.is_simulated is False):
            from elements.bme280_pressure_temperature_humidity.bme280 import (
                readBME280All
            )
            temperature, pressure, humidity = readBME280All(addr=int(os.environ["BME280_ADDRESS"], 16))
            Logger.get_instance().debug(f"BME280 : {temperature}, {pressure}, {humidity}")
        else:
            temperature = 20
            pressure = 1050
            humidity = 49.5
        misc = Miscellaneaous(pressure=pressure, humidity=humidity)
        temp = Temperature(current=Temperature.fromCelsiusToKelvin(temperature), feels_like=Temperature.calculate_feels_like(
            Temperature.fromCelsiusToKelvin(temperature), wind_speed))
        return (misc, temp)

    def read_wind(self):
        """
            Read data from the sensors (anemometer and wind vane)
            Not implemented return the default constructor of Wind
        """
        if(self.is_simulated is False):
            from elements.gy271_compass.gy271 import (
                compass
            )
            from elements.hw477_anemometer.hw477 import (
                anemometer
            )
            compass_sensor = compass(address=int(os.environ["GY271_ADDRESS"], 16))
            angle = compass_sensor.get_bearing()
            anemometer_sensor = anemometer(hallpin=int(os.environ["HW477_ADDRESS"]), magnetsNumber=int(os.environ["MAGNETS_NUMBER"]))
            rotation_speed = anemometer_sensor.readData(seconds=10)
            Logger.get_instance().debug(f"Angle : {angle}°")
            Logger.get_instance().debug(f"Speed : {rotation_speed} tr/s")
            wind_speed = 2*pi*rotation_speed*self.rotation_radius
            wind = Wind(speed=wind_speed, direction=angle)
        else:
            wind = Wind(speed=2)
        return wind

    def read_position(self):
        """
            Read data from the sensors (GPS)
            Not implemented return always the position 49°N, 1°E
        """
        position = Position(longitude=1, latitude=49)
        return position

    def run(self):
        """
            Worker main loop
        """
        # If we ask to stop reading we have to change value of has_to_read_weather to false
        while True:
            if(self.has_to_read_weather is False):
                Logger.get_instance().info(f"Killing the weather thread")
                break
            self.oneRead()
            sleep(int(self.delay_time))

    def oneRead(self):
        if(self.has_to_read_weather is True):
            weather = None
            Logger.get_instance().debug("Reading data from the sensors")
            wind = self.read_wind()
            position = self.read_position()
            (misc, temp) = self.read_pressure_temperature_humidity(wind.speed)
            weather = Weather(wind=wind, position=position,
                              misc=misc, temperature=temp)

            if(self.weather_queue is not None and self.weather_queue.full() is not True):
                self.weather_queue.put(weather)
