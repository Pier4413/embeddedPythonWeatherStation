class Miscellaneaous:
    """
      This class represents all misc data for weather like pressure, humidity, ...

      :author: Panda <panda@delmasweb.net>
      :date: January 31, 2022
      :version: 1.0
    """

    def __init__(self, pressure: int = -1, humidity: int = -1):
        """
          Constructor

          :param pressure: Optional; Default : -1; Place's pressure
          :type pressure: int
          :param humidity: Optional; Default : -1; Place's humidity
          :type humidity: int
        """
        self.pressure = pressure
        self.humidity = humidity

    def __str__(self) -> str:
        """
          Return the class as a string

          :rtype: str
        """
        return "Pressure : ["+str(self.pressure)+"], Humidity : ["+str(self.humidity)+"]"

    def __dict__(self) -> dict:
        return {
            "pressure": self.pressure,
            "humidity": self.humidity
        }
