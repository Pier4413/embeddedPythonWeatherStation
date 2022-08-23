from tkinter import * 

from functions.loading import start
from functions.slider import getValue
from modules.logger.logger import Logger

from modules.settings.settings import Settings

start()

try:
  with open(Settings.get_instance().get("general", "simu_file", None)) as file:

    fenetre = Tk()

    label = Label(fenetre, text=file.readline())
    label.pack()

    sli1 = Scale(fenetre, from_=10, to=100, tickinterval=10, orient=VERTICAL, bg = "RED", command=getValue)
    sli1.place(relx=0.15,rely=0.06,relwidth=10)
    sli1.pack()
    fenetre.mainloop()
except Exception as e:
  Logger.get_instance().error(e)