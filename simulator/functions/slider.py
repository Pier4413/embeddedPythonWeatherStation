
from tkinter import Scale

from modules.logger.logger import Logger

def getValue(event):
  Logger.get_instance().info(event)
