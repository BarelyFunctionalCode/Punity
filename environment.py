import numpy as np
import pyautogui

from utils import Vector2

class Environment:
  def __init__(self):
    size = pyautogui.size()

    self.x = 0
    self.y = 0
    self.width = size.width # 1980
    self.height = size.height # 1080
    self.objects = np.array([])

  @property
  def mouse_position(self):
    return Vector2(pyautogui.position())

Instance = Environment()
