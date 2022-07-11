import unittest
from classes.element.position import Position

class TestPosition(unittest.TestCase):
    """
        This class is a test for the Position element

        :author: Panda <panda@delmasweb.net>
        :date: January 31, 2022
        :version: 1.0
    """
    __lat = 1.0
    __lon = 2.0

    def setUp(self) -> None:
        """
            Setup
        """
        super().setUp()
        self.pos = Position(self.__lon, self.__lat)

    def test_lat(self):
        """
            Test for get latitude
        """
        self.assertEqual(self.pos.latitude, self.__lat, "Should be "+str(self.__lat))

    def test_lon(self):
        """
            Test for get longitude
        """
        self.assertEqual(self.pos.longitude, self.__lon, "Should be "+str(self.__lon))

    def test_to_string(self):
        """
            Test for string reduction of the Position class
        """
        self.assertEqual(self.pos.__str__(), "Longitude : ["+str(self.__lon)+"], Latitude : ["+str(self.__lat)+"]")