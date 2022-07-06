import unittest
from ddt import ddt, data
from classes.element.wind import Wind

@ddt
class WindTest(unittest.TestCase):
    """
        This class is a test for the Wind element

        :author: Panda <panda@delmasweb.net>
        :date: January 31, 2022
        :version: 1.0
    """
    def setUp(self) -> None:
        """
            Setup
        """
        super().setUp()
        self.wind = Wind()

    def test_speed(self):
        """
            This function test speed
        """
        self.wind.speed = 10
        self.assertEquals(self.wind.speed, 10, "Should be 10")

    def test_direction_value_ok(self):
        """
            This function test direction
        """
        self.wind.direction = 10
        self.assertEquals(self.wind.direction, 10, "Should be 10")

    def test_direction_value_up_360(self):
        """
            This function test direction if the value is up 360°, should return the value - 360
        """
        self.wind.direction = 460
        self.assertEquals(self.wind.direction, 100, "Should be 100")

    def test_direction_value_down_0(self):
        """
            This function test direction if the value is below 360°, should return the value + 360
        """
        self.wind.direction = -50
        self.assertEquals(self.wind.direction, 310, "Should be 310")

    @data(0, 45, 90, 135, 180, 225, 270, 315)
    def test_convert_direction_degrees_to_string(self, value):
        """
            Test for conversion from degrees in direction to position on compass rose
        """
        result = Wind.convertDirectionDegreesInDirectionString(value)
        if(value == 0):
            self.assertEquals(result, "n", "Should return n")
        elif(value == 45):
            self.assertEquals(result, "ne", "Should return ne")
        elif(value == 90):
            self.assertEquals(result, "e", "Should return e")
        elif(value == 135):
            self.assertEquals(result, "se", "Should return se")
        elif(value == 180):
            self.assertEquals(result, "s", "Should return s")
        elif(value == 225):
            self.assertEquals(result, "sw", "Should return sw")
        elif(value == 270):
            self.assertEquals(result, "w", "Should return w")
        elif(value == 315):
            self.assertEquals(result, "nw", "Should return nw")
        else:
            self.assertTrue(False)

    def test_convert_speed_from_meter_seconds_to_kilometers_hours(self):
        """
            This function test to convert in m/s to km/h
        """
        self.assertEquals(Wind.convertSpeedFromMeterSecondsToKilometersHours(5), 18, "Should return 18")