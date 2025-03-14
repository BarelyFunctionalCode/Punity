import tkinter as tk

from environment import Instance as environment

from objects.object import Object
from objects.fren import Fren
from objects.border import Border
from control_menu import ControlMenu

if __name__ == "__main__":

  # Root object for all other objects to spawn from
  root = Object()

  # Create the control menu
  ControlMenu(root.tk_obj)

  # Create the border objects for the screen
  Border(root, environment.width, environment.height, environment.x, environment.y, 50)

  # Create the fren object
  # Fren(root)
  Fren(root, 'hole_punch')


  # root.print_hierarchy()

  # Run the main loop
  root.begin()