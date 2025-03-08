import tkinter as tk

from environment import Instance as environment

from objects.fren import Fren
from objects.border import Border


from effects.hole_punch import HolePunch

from utils import invis_tk

if __name__ == "__main__":
  # Create the border objects for the screen
  Border(environment.x, environment.y, environment.width, environment.height, 50)

  # Root object for all other objects to spawn from
  root = invis_tk(tk.Tk())

  # Create the fren object
  Fren('fren', root)

  # Test hole punch
  HolePunch(root, [0,0, 100,50, 200,0, 130,130, 200,200, 0,200], 500, 100, 5000)
  HolePunch(root, [0,50, 50,0, 100,0, 150,70, 120,100, 80,150, 30,100], 700, 300, 8000)

  # Run the main loop
  try:
    root.mainloop()
  except:
    root.destroy()
    root = None