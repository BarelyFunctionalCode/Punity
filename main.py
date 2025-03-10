import tkinter as tk

from environment import Instance as environment

from objects.fren import Fren
from objects.border import Border

from objects.screen_chunk import ScreenChunk

from utils import invis_tk, Vector2

if __name__ == "__main__":
  # Create the border objects for the screen
  Border(environment.x, environment.y, environment.width, environment.height, 50)

  # Root object for all other objects to spawn from
  root = invis_tk(tk.Tk())

  # Create the fren object
  # Fren(root)
  Fren(root, 'hole_punch')

  # Create the screen chunk object
  # ScreenChunk(root, [0,0, 200,0, 200,200, 0,200, 0,0], 500, 300, 5000, False, True, Vector2([500, 500]), Vector2([100, 100]))

  # Run the main loop
  try:
    root.mainloop()
  except:
    root.destroy()
    root = None