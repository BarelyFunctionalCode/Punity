import numpy as np
import pyautogui
import Quartz
import time

from utils import Vector2

class ExternalApplication:
  def __init__(self, name, width, height, x, y):
    self.name = name
    self.position = Vector2([x, y])
    self.size = Vector2([width, height])
    self.last_update = time.time()
    

class Environment:
  def __init__(self):
    size = pyautogui.size()

    self.x = 0
    self.y = 25
    self.width = size.width
    self.height = size.height-25 # TODO: Find a better way to offset the taskbar
    self.paused = False
    self.objects = np.array([])
    self.root = None
    self.applications = {}

  def update(self):
    self.update_applications()
    self.root.tk_obj.after(100, self.update)

  def set_root(self, root):
    self.root = root
    self.update()

  def update_applications(self):
    windows = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListExcludeDesktopElements | Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)
    for window in windows:
      name = window[Quartz.kCGWindowName]
      width = window[Quartz.kCGWindowBounds]['Width']
      height = window[Quartz.kCGWindowBounds]['Height']
      x = window[Quartz.kCGWindowBounds]['X']
      y = window[Quartz.kCGWindowBounds]['Y']
      if y > 0 and width > 100 and height > 100 and name != "" and name != 'Notification Center' and "punity_" not in name: 
        if name not in self.applications:
          self.applications[name] = ExternalApplication(name, width, height, x, y)
          print(f'\"{name}\" created at {self.applications[name].position} with size {self.applications[name].size}')
        else:
          new_pos = Vector2([x, y])
          new_size = Vector2([width, height])
          if new_pos != self.applications[name].position or new_size != self.applications[name].size:
            self.applications[name].last_update = time.time()
            print(f'\"{name}\" moved to {new_pos} with size {new_size}')

          self.applications[name].position = new_pos
          self.applications[name].size = new_size

    window_names = [window[Quartz.kCGWindowName] for window in windows]
    delete_keys = []
    for app in self.applications.keys():
      if app not in window_names:
        delete_keys.append(app)
    for key in delete_keys:
      del self.applications[key]

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
