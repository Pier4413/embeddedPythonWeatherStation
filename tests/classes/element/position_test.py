import unittest
from classes.element.position import Position

class TestPosition(unittest.TestCase):
    """
        This class is a test for the Position element

        :author: Panda <panda@delmasweb.net>
        :date: January 31, 2022
        :version: 1.0
    """
    __name = "Test"
    __code = "FR"
    __id = 152
    __lat = 1.0
    __lon = 2.0

    def setUp(self) -> None:
        """
            Setup
        """
        super().setUp()
        self.pos = Position(self.__name, self.__code, self.__id, self.__lon, self.__lat)

    def test_name(self):
        """
            Test for get name
        """
        self.assertEquals(self.pos.name, self.__name, "Should be "+self.__name)

    def test_code(self):
        """
            Test for get code
        """
        self.assertEquals(self.pos.country, self.__code, "Should be "+str(self.__code))

    def test_id(self):
        """
            Test for get id
        """
        self.assertEquals(self.pos.id, self.__id, "Should be "+str(self.__id))

    def test_lat(self):
        """
            Test for get latitude
        """
        self.assertEquals(self.pos.latitude, self.__lat, "Should be "+str(self.__lat))

    def test_lon(self):
        """
            Test for get longitude
        """
        self.assertEquals(self.pos.longitude, self.__lon, "Should be "+str(self.__lon))

    def test_to_string(self):
        """
            Test for string reduction of the Position class
        """
        self.assertEquals(self.pos.__str__(), "Name : ["+self.__name+"], Country : ["+self.__code+"], Id : ["+str(self.__id)+"], Longitude : ["+str(self.__lon)+"], Latitude : ["+str(self.__lat)+"]")