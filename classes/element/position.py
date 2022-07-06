class Position:
    """
      This class represents a geographical position

      :author: Panda <panda@delmasweb.net>
      :date: January 15, 2022
      :version: 1.0
    """

    def __init__(self, longitude: float = 0.0, latitude: float = 0.0):
        """
          Constructor

          :param longitude: City's Longitude
          :type longitude: float
          :param latitude: City's Latitude
          :param latitude: float
        """
        self.longitude = longitude
        self.latitude = latitude

    def __str__(self) -> str:
        """
          Returns values as a string

          :rtype: str
        """
        return "Longitude : ["+str(self.longitude)+"], Latitude : ["+str(self.latitude)+"]"

    def __dict__(self) -> dict:
        """
          Return the elements of the class in a dict form
        """
        return {
            "longitude": self.longitude,
            "latitude": self.latitude
        }
