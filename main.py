import tkinter as tk

from environment import Instance as environment

from objects.fren import Fren
from objects.border import Border

from utils import invis_tk

if __name__ == "__main__":
  # Create the border objects for the screen
  Border(environment.x, environment.y, environment.width, environment.height, 50)

  # Root object for all other objects to spawn from
  root = invis_tk(tk.Tk())

  # Create the fren object
  display = Fren('fren', root)

  try:
    root.mainloop()
  except:
    root.destroy()
    root = None