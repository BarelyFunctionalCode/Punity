import numpy as np
import pyautogui

from engine.math import Vector2
from engine.event import Event

from .external_application import update_applications
from .system import add_input_event_monitor


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
    self.new_application_event = Event()
    self.mouse_position = Vector2([0, 0])
    self.new_input_event = Event()

  def update(self):
    update_applications(self.applications, self.new_application_event)
    self.root.tk_obj.after(100, self.update)

  def set_root(self, root):
    self.root = root
    self.update()

  def start_input_event_monitor(self):
    add_input_event_monitor(self, self.new_input_event)
  
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
