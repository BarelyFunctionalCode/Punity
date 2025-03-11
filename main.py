import tkinter as tk

from environment import Instance as environment

from objects.fren import Fren
from objects.border import Border
from control_menu import ControlMenu

from utils import invis_tk

if __name__ == "__main__":

  # Root object for all other objects to spawn from
  root = invis_tk(tk.Tk())

  # Create the control menu
  ControlMenu(root)

  # Create the border objects for the screen
  Border(root, environment.width, environment.height, environment.x, environment.y, 50)

  # Create the fren object
  # Fren(root)
  Fren(root, 'hole_punch')


  # Run the main loop
  try:
    root.mainloop()
  except:
    root.destroy()
    root = None