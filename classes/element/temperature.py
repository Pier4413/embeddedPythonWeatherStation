class Temperature:
    """
      This class represents all data on temperature. All values are supposed to be in Kelvin

      :author: Panda <panda@delmasweb.net>
      :date: 23 Janvier 2022
      :version: 1.0
    """

    def __init__(self, current: float = -1, feels_like: float = -1) -> None:
        """
            Constructor

            :param current: Optional; Default : -1; Current temperature in Kelvin
            :type current: float
            :param feels_like: Optional; Default : -1; Current temperature in Kelvin
            :type feels_like: float
        """
        self.current = current
        self.feels_like = feels_like

    def __str__(self) -> str:
        """
            Return the class as a string

            :rtype: str
        """
        return "Current : ["+str(self.current)+"], Feels like : ["+str(self.feels_like)+"]"

    def __dict__(self) -> dict:
        """
            Return the elements of the class in a dict form
        """
        return {
            "current": self.current,
            "feels_like": self.feels_like
        }

    def fromKelvinToCelsius(value: float) -> float:
        """
            This function convert a temperature from Kelvin to celsius

            :param value: The value to convert
            :type value: float
            :return: The converted value
            :rtype: float
            :meta static:
        """
        return round(value-273.15, 2)

    def fromCelsiusToKelvin(value: float) -> float:
        """
            This function convert a temperature from Celsius to Kelvin

            :param value: The value to convert
            :type value: float
            :return: The converted value
            :rtype: float
            :meta static:
        """
        return round(value + 273.15, 2)

    def fromCelsiusToFahrenheit(value: float) -> float:
        """
            This function convert a temperature from Celsius to Fahrenheit

            :param value: The value to convert
            :type value: float
            :return: The converted value
            :rtype: float
            :meta static:
        """
        return round(value * 1.8 + 32, 2)

    def fromFahrenheitToCelsius(value: float) -> float:
        """
            This function convert a temperature from Fahrenheit to Celsius

            :param value: The value to convert
            :type value: float
            :return: The converted value
            :rtype: float
            :meta static:
        """
        return round((value - 32)/1.8, 2)

    def fromFahrenheitToKelvin(value: float) -> float:
        """
          This function convert a temperature from Fahrenheit to Kelvin

          :param value: The value to convert
          :type value: float
          :return: The converted value
          :rtype: float
          :meta static:
        """
        return round(Temperature.fromCelsiusToKelvin(Temperature.fromFahrenheitToCelsius(value)), 2)

    def fromKelvinToFahrenheit(value: float) -> float:
        """
          This function convert a temperature from Kelvin to Fahrenheit

          :param value: The value to convert
          :type value: float
          :return: The converted value
          :rtype: float
          :meta static:
        """
        return round(Temperature.fromCelsiusToFahrenheit(Temperature.fromKelvinToCelsius(value)), 2)

    def calculate_feels_like(value: float, wind_speed: float):
        """
          :param value: The value of temperature to convert to a "feels_like" (Wind chill) in Kelvin
          :type value: float
          :param wind_speed: The value of the wind for calculation in m/s
          :type wind_speed: float
          :return: The value of feels_like in Kelvin
        """
        if(3.6 * wind_speed < 4.8):
            feels_like_celsius = Temperature.fromKelvinToCelsius(
                value) + 0.2 * (0.1345 * Temperature.fromKelvinToCelsius(value) - 1.59) * 3.6 * wind_speed
        else:
            feels_like_celsius = 13.12 + (0.6215 * Temperature.fromKelvinToCelsius(value)) + (
                (0.3965 * Temperature.fromKelvinToCelsius(value) - 11.37) * pow(3.6 * wind_speed, 0.16))
        return Temperature.fromCelsiusToKelvin(feels_like_celsius)
