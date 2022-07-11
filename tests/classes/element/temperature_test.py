import unittest
from ddt import ddt, data
from classes.element.temperature import Temperature

@ddt
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
        self.assertEqual(self.temp.current, 10, "Should be 10")

    def test_feels_like(self):
        """
            Test getter and setter for feels like
        """
        self.temp.feels_like = 10
        self.assertEqual(self.temp.feels_like, 10, "Should be 10")

    def test_to_string(self):
        """
            Test to string for temperature
        """
        self.assertEqual(self.temp.__str__(), "Current : [-1], Feels like : [-1]")

    def test_kelvin_to_celsius(self):
        """
            Test the conversion from Celsius to Kelvin
        """
        self.assertEqual(Temperature.fromKelvinToCelsius(10), -263.15, "Should be -263.15")

    def test_celsius_to_kelvin(self):
        """
            Test the conversion from Celsius to Kelvin
        """
        self.assertEqual(Temperature.fromCelsiusToKelvin(100), 373.15, "Should be 373.15")

    def test_celsius_to_fahrenheit(self):
        """
            Test the conversion from Celsius To Fahrenheit
        """
        self.assertEqual(Temperature.fromCelsiusToFahrenheit(10), 50.0, "Should be 50.0")

    def test_fahrenheit_to_celsius(self):
        """
            Test the conversion from Fahrenheit To Celsius
        """
        self.assertEqual(Temperature.fromFahrenheitToCelsius(10), -12.22, "Should be -12.22")

    def test_kelvin_to_fahrenheit(self):
        """
            Test the conversion from Kelvin To Fahrenheit
        """
        self.assertEqual(Temperature.fromKelvinToFahrenheit(10), -441.67, "Should be -441.67")

    def test_fahrenheit_to_kelvin(self):
        """
            Test the conversion from Fahrenheit To Kelvin
        """
        self.assertEqual(Temperature.fromFahrenheitToKelvin(10), 260.93, "Should be 260.93")

    @data([273.15, 10], [283.15, 10])
    def test_calculate_feels_like(self, value):
        #279.35
        result = Temperature.calculate_feels_like(value=value[0], wind_speed=value[1])
        if(value[0] == 273.15):
            self.assertAlmostEqual(first=result, second=266.15, msg="Should be 266.15K", delta=0.2)
        elif(value[0] == 283.15):
            self.assertAlmostEqual(first=result, second=279.35, msg="Should be 279.35K", delta=0.2)
        else:
            self.assertTrue(False)