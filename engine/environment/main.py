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

    self.dev_mode = False
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

    self.inactivity_timeout = 10000
    self.inactivity_timer = 0
    self.inactivity_event = Event()

    self.mouse_position = Vector2([0, 0])
    self.new_input_event = Event()
    self.new_input_event.add_listener(self._parse_keyboard_text)

    self.keyboard_current_log = ''
    self.keyboard_current_log_window = -1
    self.keyboard_log_history = []


  def update(self):
    update_applications(self.applications, self.new_application_event)

    # TODO: If current keyboard log has sat for log enough, send event for current log and start new one
    if self.inactivity_timer > self.inactivity_timeout:
      if self.keyboard_current_log != '':
        self._new_keyboard_log(time.time())

      self.inactivity_event.invoke({
        'timestamp': time.time(),
        'type': 'inactivity',
        'pid': self.active_application_pid,
      })
      self.inactivity_timer = -1
    elif self.inactivity_timer != -1:
      self.inactivity_timer += 100
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
    self.inactivity_timer = 0
    self.active_application_pid = app_pid

  def _parse_keyboard_text(self, event_data):
    self.inactivity_timer = 0
    if event_data['type'] == 'key_down':
      # If enough time has passed since the last key event, treat it as a new log
      # If the active application has changed since the last keyboard input, treat it as a new log
      # Enter key triggers an event
      if len(self.keyboard_current_log) != 0 and (self.keyboard_current_log_window != self.active_application_pid or event_data['key'] == '\r') :
        self._new_keyboard_log(event_data['timestamp'])
      if event_data['key'] == '\r': return
      # Handle other keys
      if event_data['key'] == '\x7f': # Backspace
        if len(self.keyboard_current_log) > 0:
          self.keyboard_current_log = self.keyboard_current_log[:-1]
      elif event_data['key'] == '\x1b' or event_data['key'] == '\x03' or event_data['key'] == '\x18': # Escape or Ctrl+C or Ctrl+X
        self.keyboard_current_log = ''
      else:
        self.keyboard_current_log += event_data['key']
      
      self.keyboard_current_log_window = self.active_application_pid

  def _new_keyboard_log(self, timestamp):
    self.keyboard_log_history.append(self.keyboard_current_log)
    self.keyboard_current_log = ''
    self.new_input_event.invoke({
      'timestamp': timestamp,
      'type': 'keyboard_log',
      'text': self.keyboard_log_history[-1],
      'pid': self.keyboard_current_log_window,
    })
Instance = Environment()