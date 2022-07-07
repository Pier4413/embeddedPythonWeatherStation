import RPi.GPIO as gpio
import time

class anemometer:

  def __init__(self, hallpin: int = 12, magnetsNumber: int = 4, step_time: float = 0.1, reading_time: float = 10) -> None:
    self.hallpin = hallpin
    self.magnetsNumber = magnetsNumber
    self.step_time = step_time
    self.reading_time = reading_time
    gpio.setmode(gpio.BOARD)
    gpio.setwarnings(False)
    gpio.setup(self.hallpin, gpio.IN)

  def readData(self) -> int:
    """
      Read the numbers of passing through the sensors and send back the speed of magnets with the number of magnets

      :param seconds: The number of seconds to read
      :type seconds: int
    """
    start = time.time()
    end = time.time()
    counter = 0
    while((end - start) < self.reading_time):
      end = time.time()
      if(gpio.input(self.hallpin) == False):
        counter = counter + 1
      time.sleep(self.step_time)
    return counter/(self.magnetsNumber*self.reading_time)
