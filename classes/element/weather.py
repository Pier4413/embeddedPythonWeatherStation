from .wind import Wind
from .position import Position
from .temperature import Temperature
from .miscellaneous import Miscellaneaous


class Weather:
    """
        This class represents a weather (wind, position, temperature, pressure, ...)

        :author: Panda <panda@delmasweb.net>
        :date: 23 Janvier 2022
        :version: 1.0
    """

    def __init__(self, wind: Wind = None, position: Position = None, temperature: Temperature = None, misc: Miscellaneaous = None) -> None:
        """
            Constructor

            :param wind: Optional; Default : None; Place's Wind
            :type wind: Wind
            :param position: Optional; Default : None; Position 
            :type position: Position
            :param temperature: Optional; Default : None; Place's temperature
            :type temperature: Temperature
            :param misc: Optional; Default : None; Place's misc data
            :type misc: Miscellaneaous
        """
        self.wind = wind
        self.position = position
        self.temperature = temperature
        self.misc = misc

    def __str__(self) -> str:
        """
            Return the class as a string

            :rtype: str
        """
        return "Wind : ["+str(self.wind)+"], Position : ["+str(self.position)+"], Temperature : ["+str(self.temperature)+"], Misc : ["+str(self.misc)+"]"

    def __dict__(self) -> dict:
        """
            Return the elements of the class in a dict form
        """
        return {
            "misc": self.misc.__dict__(),
            "temperature": self.temperature.__dict__(),
            "wind": self.wind.__dict__(),
            "position": self.position.__dict__()
        }
