import time
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
    self.active_application_pid = -1
    self.new_application_event = Event()
    self.new_application_event.add_listener(self._track_new_application)

    self.mouse_position = Vector2([0, 0])
    self.new_input_event = Event()
    self.new_input_event.add_listener(self._parse_keyboard_text)

    self.keyboard_new_log_timeout = 20
    self.keyboard_last_event_time = 0
    self.keyboard_current_log = ''
    self.keyboard_log_history = []

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


  def _track_new_application(self, app_pid):
    self.active_application_pid = app_pid

  def _parse_keyboard_text(self, event_data):
    if event_data['type'] == 'key_down':
      self.keyboard_last_event_time = event_data['timestamp']

      # If enough time has passed since the last key event, treat it as a new log
      if time.time() - self.keyboard_last_event_time > self.keyboard_new_log_timeout:
        self.keyboard_log_history.append(self.keyboard_current_log)
        self.keyboard_current_log = ''

      # Enter key triggers an event
      if event_data['key'] == '\r':
        if len(self.keyboard_current_log) == 0:
          return
        self.keyboard_log_history.append(self.keyboard_current_log)
        self.keyboard_current_log = ''
        self.new_input_event.invoke({
          'timestamp': event_data['timestamp'],
          'type': 'keyboard_log',
          'text': self.keyboard_log_history[-1],
          'window': self.applications[self.active_application_pid].name if self.active_application_pid != -1 else 'Unknown',
        })
      # Handle other keys
      elif event_data['key'] == '\x7f': # Backspace
        if len(self.keyboard_current_log) > 0:
          self.keyboard_current_log = self.keyboard_current_log[:-1]
      elif event_data['key'] == '\x1b' or event_data['key'] == '\x03' or event_data['key'] == '\x18': # Escape or Ctrl+C or Ctrl+X
        self.keyboard_current_log = ''
      else:
        self.keyboard_current_log += event_data['key']

Instance = Environment()
