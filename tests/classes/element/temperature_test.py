import unittest
from classes.element.temperature import Temperature

class TestTemperature(unittest.TestCase):
    """
        This class is a test for the Temperature element

        :author: Panda <panda@delmasweb.net>
        :date: January 31, 2022
        :version: 1.0
    """

    def setUp(self):
        """
            Setup
        """
        super().setUp()
        self.temp = Temperature()

    def test_current(self):
        """
            Test getter and setter for current
        """
        self.temp.current = 10
        self.assertEquals(self.temp.current, 10, "Should be 10")

    def test_feels_like(self):
        """
            Test getter and setter for feels like
        """
        self.temp.feels_like = 10
        self.assertEquals(self.temp.feels_like, 10, "Should be 10")

    def test_max(self):
        """
            Test getter and setter for max
        """
        self.temp.max = 10
        self.assertEquals(self.temp.max, 10, "Should be 10")

    def test_min(self):
        """
            Test getter and setter for current
        """
        self.temp.min = 10
        self.assertEquals(self.temp.min, 10, "Should be 10")

    def test_to_string(self):
        """
            Test to string for temperature
        """
        self.assertEquals(self.temp.__str__(), "Current : [-1], Min : [-1], Max : [-1], Feels like : [-1]")

    def test_kelvin_to_celsius(self):
        """
            Test the conversion from Celsius to Kelvin
        """
        self.assertEquals(Temperature.fromKelvinToCelsius(10), -263.15, "Should be -263.15")

    def test_celsius_to_kelvin(self):
        """
            Test the conversion from Celsius to Kelvin
        """
        self.assertEquals(Temperature.fromCelsiusToKelvin(100), 373.15, "Should be 373.15")

    def test_celsius_to_fahrenheit(self):
        """
            Test the conversion from Celsius To Fahrenheit
        """
        self.assertEquals(Temperature.fromCelsiusToFahrenheit(10), 50.0, "Should be 50.0")

    def test_fahrenheit_to_celsius(self):
        """
            Test the conversion from Fahrenheit To Celsius
        """
        self.assertEquals(Temperature.fromFahrenheitToCelsius(10), -12.22, "Should be -12.22")

    def test_kelvin_to_fahrenheit(self):
        """
            Test the conversion from Kelvin To Fahrenheit
        """
        self.assertEquals(Temperature.fromKelvinToFahrenheit(10), -441.67, "Should be -441.67")

    def test_fahrenheit_to_kelvin(self):
        """
            Test the conversion from Fahrenheit To Kelvin
        """
        self.assertEquals(Temperature.fromFahrenheitToKelvin(10), 260.93, "Should be 260.93")