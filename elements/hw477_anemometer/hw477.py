import RPi.GPIO as gpio
import time

class anemometer:

  def __init__(self, hallpin: int = 12, magnetsNumber: int = 4) -> None:
    self.hallpin = hallpin
    self.magnetsNumber = magnetsNumber
    gpio.setmode(gpio.BOARD)
    gpio.setwarnings(False)
    gpio.setup(self.hallpin, gpio.IN)

  def readData(self, seconds: int = 10) -> int:
    """
      Read the numbers of passing through the sensors and send back the speed of magnets with the number of magnets

      :param seconds: The number of seconds to read
      :type seconds: int
    """
    start = time.time()
    end = time.time()
    counter = 0
    print(f"{start} {end}")
    while((end - start) < seconds):
      end = time.time()
      if(gpio.input(self.hallpin) == False):
        counter = counter + 1
      time.sleep(0.1)
    return counter/(self.magnetsNumber*seconds)
