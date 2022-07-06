class Wind:
    """
        This represent a wind (direction and speed)

        :author: Panda <panda@delmasweb.net>
        :date: 23 Janvier 2022
        :version: 1.0
    """

    def __init__(self, speed: float = 0, direction: int = 0) -> None:
        """
            Constructor

            :param speed: Optional; Default : 0; Wind's speed
            :type speed: float
            :param direction: Optional; Default : 0; Wind's direction in degrees relative to North (0 : North, 90 : East, 180 : South, 270 : West)
            :type direction: int
        """
        self.speed = speed
        self.__direction = direction

    def __str__(self) -> str:
        """
            Return the class as a string

            :rtype: str
        """
        return "Speed : ["+str(self.speed)+"], Direction : ["+str(self.direction)+"]"

    def __dict__(self) -> dict:
        """
            Return the elements of the class in a dict form
        """
        return {
            "speed": self.speed,
            "direction": self.direction
        }

    def set_direction(self, a) -> None:
        if(a < 0):
            self.__direction = a + 360
        elif(a > 360):
            self.__direction = a - 360
        else:
            self.__direction = a

    def get_direction(self):
        return self.__direction

    def convertDirectionDegreesInDirectionString(value: float) -> str:
        """
            This function convert an angle on the plan to the associate 8-part

            :param value: The direction
            :type value: float
            :return: The associated part in lower case as a code (ne, n, sw, ...)
            :rtype: str
        """
        if(value >= 22.5 and value < 67.5):
            return "ne"
        elif(value >= 67.5 and value < 112.5):
            return "e"
        elif(value >= 112.5 and value < 157.5):
            return "se"
        elif(value >= 157.5 and value < 202.5):
            return "s"
        elif(value >= 202.5 and value < 247.5):
            return "sw"
        elif(value >= 247.5 and value < 292.5):
            return "w"
        elif(value >= 292.5 and value < 337.5):
            return "nw"
        else:
            return "n"

    def convertSpeedFromMeterSecondsToKilometersHours(value: float) -> float:
        return round(value * 3.6, 2)

    direction = property(get_direction, set_direction,
                         doc="Direction is a special property with some securities on it (can't be negative, neither upper than 360°)")
