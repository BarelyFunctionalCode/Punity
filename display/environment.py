import numpy as np
import pyautogui

class Environment:
  def __init__(self):
                           # top, left, bottom, right
    self.bounds = np.array([-1080, 1920, 1080, 0])

  @property
  def mouse_position(self):
    return np.array(pyautogui.position())

  def is_in_bounds(self, position):
    return self.bounds[0] < position[1] < self.bounds[2] and self.bounds[3] < position[0] < self.bounds[1]

Instance = Environment()