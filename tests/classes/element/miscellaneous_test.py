import unittest
from classes.element.miscellaneous import Miscellaneaous

class TestMiscellaneous(unittest.TestCase):

    """
        This class is a test for the Miscellaneous element

        :author: Panda <panda@delmasweb.net>
        :date: January 31, 2022
        :version: 1.0
    """
    def setUp(self):
        """
            Setup
        """
        super().setUp()
        self.misc = Miscellaneaous()

    def test_pressure(self):
        """
            Test for set and get pressure
        """
        self.misc.pressure = 10
        self.assertEquals(self.misc.pressure, 10, "Should be 10")

    def test_humidity(self):
        """
            Test for set and get humidity
        """
        self.misc.humidity = 10
        self.assertEquals(self.misc.humidity, 10, "Should be 10")
    
    def test_to_string(self):
        """
            Test for string reduction of the Misc class
        """
        self.assertEquals(self.misc.__str__(), "Pressure : [-1], Humidity : [-1], Sunrise : [-1], Sunset : [-1]")

   