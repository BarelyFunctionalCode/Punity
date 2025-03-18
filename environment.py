import numpy as np
import pyautogui

from utils import Vector2

class Environment:
  def __init__(self):
    size = pyautogui.size()

    self.x = 0
    self.y = 0
    self.width = size.width
    self.height = size.height-25 # TODO: Find a better way to offset the taskbar
    self.paused = False
    self.objects = np.array([])
    self.root = None

  @property
  def mouse_position(self):
    return Vector2(pyautogui.position())
  
  def get_object(self, name):
    for obj in self.objects:
      if obj.name == name:
        return obj
  
  def pause(self):
    self.paused = True
    for obj in self.objects:
      obj.paused = True

  def resume(self):
    self.paused = False
    for obj in self.objects:
      obj.paused = False

Instance = Environment()
