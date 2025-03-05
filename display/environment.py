import numpy as np
import pyautogui

from .utils import Vector2

class Environment:
  def __init__(self):
                           # top, left, bottom, right
    self.bounds = np.array([-1080, 1920, 1080, 0])

  @property
  def mouse_position(self):
    return Vector2(pyautogui.position())

  def is_in_bounds(self, position):
    return self.bounds[0] < position.y < self.bounds[2] and self.bounds[3] < position.x < self.bounds[1]

Instance = Environment()