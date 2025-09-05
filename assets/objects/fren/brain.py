import tkinter as tk
import threading
import json
import time

from engine import Component, Environment, Event

from .ai_interface import analyze_data

class Brain(Component):
  """
  The Brain class is responsible for monitoring user activity and generating insights based on that activity.
  Insights are initially generated for individual apps, then if a group of related apps are detected, the generated
  app insights are used to generate an insight for the group of apps, otherknown as an activity.

  General workflow:
  1. For any input event, the data is collected and organized per app.
  2. If the user is inactive or switches to a different application, a new insight is attemoted for that app.
  3. If the cooldown period has passed, the app data is sent to the AI model for analysis and returns an insight.
  4. The insight is stored in the data dictionary and can be accessed later.
  5. After the app insight is generated, an activity insight is attempted.
  6. If the cooldown period has passed, the activity data is sent to the AI model for analysis and returns an insight.
  7. The insight is stored in the data dictionary and can be accessed later.
  8. After a certain threshold of app and activity insights have been generated, Fren can then communicate with the user
  knowing the context of what they are doing.

  At certain thresholds, the histories of app and activity insights are sent to the AI model for consolidation and
  summarization. This is done to reduce the amount of data that needs to be stored and to provide a more concise
  summary of the user's activity.
  """
  def __init__(self, **kwargs):
    self.is_enabled = kwargs.get('use_brain', True)
    self.data = {
      'apps': {},
      'activities': []
    }

    self.is_ai_processing_locked = False

    self.last_event_pid = -1
    self.last_event_time = 0

    if Environment.dev_mode:
      with open('temp.json', 'w') as f:
        json.dump([], f)

    # Event that is triggered after an app insight is generated and stored
    self.new_app_insight_event = Event()
    self.new_app_insight_event.add_listener(self._get_activity_insight)
    self.app_insight_cooldown = 300.0

    # Hyperparameters for handling related app cohesion
    self.related_app_frequency_multiplier = 1.5
    self.related_app_frequency_decay = 0.8
    self.related_app_frequency_threshold = 5.0

    # Event that is triggered after an activity insight is generated and stored
    self.new_activity_insight_event = Event()
    self.activity_insight_cooldown = 600.0
    
    super().__init__()

  def start(self):
    super().start()
    if not self.is_enabled:
      return
    Environment.new_input_event.add_listener(self._ingest_input_event)
    Environment.inactivity_event.add_listener(self._inactivity_event)

  def update(self):
    super().update()

  def _ingest_input_event(self, event_data):
    # Get data that would be given for any input event
    pid = event_data['pid']
    timestamp = event_data['timestamp']
    app_name = Environment.applications[pid].name if pid != -1 else 'Unknown'
    app_title = Environment.applications[pid].title if pid != -1 else 'Unknown'

    # Create entry in data['apps'] dict if it doesn't exist
    if pid not in self.data['apps']:
      found = False
      for existing_pid in self.data['apps']:
        if self.data['apps'][existing_pid]['app_name'] == app_name:
          pid = existing_pid
          found = True
          break
      if not found:
        self.data['apps'][pid] = {
          'app_name': app_name,
          'input_sequence': [],
          'related_app_pids': {},
          'total_clicks': 0,
          'active_time_seconds': 0,
          'insight': {
            'value': None,
            'timestamp': 0,
            'history': []
          }
      }
    
    # Update data from relevent input event
    self.data['apps'][pid]['app_title'] =  app_title
    self.data['apps'][pid]['last_active_time'] =  timestamp

    # Update related app pids
    if self.last_event_pid != -1 and self.last_event_pid != pid:
      if self.last_event_pid in self.data['apps'][pid]['related_app_pids']:
        self.data['apps'][pid]['related_app_pids'][self.last_event_pid] *= self.related_app_frequency_multiplier
      else:
        self.data['apps'][pid]['related_app_pids'][self.last_event_pid] = 1.0

      for related_pid in self.data['apps'][pid]['related_app_pids']:
        if related_pid != self.last_event_pid:
          self.data['apps'][pid]['related_app_pids'][related_pid] *= self.related_app_frequency_decay

    # Process input event data
    input_data = None
    if event_data['type'] == 'keyboard_log':
      input_data = {
        'type': 'text',
        'data': event_data['text'],
      }
    elif event_data['type'] == 'mouse_down':
      input_data = {
        'type': 'mouse_click',
        'data': event_data['button'],
      }
      self.data['apps'][pid]['total_clicks'] += 1

    if input_data:
      self.data['apps'][pid]['input_sequence'].append(input_data)

    if self.last_event_pid == pid:
      self.data['apps'][pid]['active_time_seconds'] += (timestamp - self.last_event_time)
    else:
      self._get_app_insight(self.last_event_pid)

    self.last_event_pid = pid
    self.last_event_time = timestamp

  def _inactivity_event(self, event_data):
    # Get trigger an app insight for the app that was last active
    if Environment.dev_mode:
      with open('temp.json', 'r') as f:
        temp_data = json.load(f)
      with open('temp.json', 'w') as f:
        temp_data.append(self.data)
        json.dump(temp_data, f, indent=2)
    pid = event_data['pid']
    self._get_app_insight(pid)
    
  def _get_app_insight(self, pid):
    if pid not in self.data['apps']:
      print(f"App {pid} not found in data, skipping insight")
      return
    if self.data['apps'][pid]['insight']['value'] and \
        time.time() - self.data['apps'][pid]['insight']['timestamp'] < self.app_insight_cooldown:
      print(f"Insight for {self.data['apps'][pid]['app_name']} is still valid")
      return
    if self.is_ai_processing_locked:
      print(f"AI is already processing data, skipping app insight for {self.data['apps'][pid]['app_name']}")
      return
    self.is_ai_processing_locked = True

    # Data that is not included in AI prompt
    ignore_keys = ['total_clicks', 'last_active_time', 'insight']
    
    # Check if app insight cooldown has passed
    print(f"Getting insight for {self.data['apps'][pid]['app_name']}")

    # Building the data to be sent to the AI
    app_data = self.data['apps'][pid]
    app_data = {k: v for k, v in app_data.items() if k not in ignore_keys}

    # Function to set the insight that is returned from the AI
    def set_insight(insight):
      self.is_ai_processing_locked = False
      if insight is None:
        print(f"Insight for {self.data['apps'][pid]['app_name']} is None")
        return
      if 'insight' in self.data['apps'][pid]:
        self.data['apps'][pid]['insight']['history'].append({
          'value': self.data['apps'][pid]['insight']['value'],
          'timestamp': self.data['apps'][pid]['insight']['timestamp']
        })
        self.data['apps'][pid]['insight']['value'] = insight
        self.data['apps'][pid]['insight']['timestamp'] = time.time()

      self.new_app_insight_event.invoke(pid)

    # In a new thread, call analyze_data with the app_data
    threading.Thread(target=analyze_data, args=("app_insight", app_data, set_insight)).start()

  def _get_activity_insight(self, pid):
    if pid not in self.data['apps']:
      print(f"App {pid} not found in data, skipping activity insight")
      return None
    
    # Gather data of apps that were used in the same time period as this app
    related_apps_pids = [ check_pid for check_pid, check_app in self.data['apps'].items() \
      if pid != check_pid and pid in check_app['related_app_pids'] and \
      check_app['related_app_pids'][pid] >= self.related_app_frequency_threshold ]

    if len(related_apps_pids) == 0:
      print(f"No related apps found for {self.data['apps'][pid]['app_name']}")
      return
    
    # Check if activity insight cooldown has passed
    activity_app_pids = [pid, *related_apps_pids]
    activity_app_names = set([self.data['apps'][activity_app_pid]['app_name'] for activity_app_pid in activity_app_pids])
    for activity in self.data['activities']:
        if activity_app_names.issubset(activity['app_names']) or activity['app_names'].issubset(activity_app_names):
          if activity['insight']['value'] and \
              time.time() - activity['insight']['timestamp'] < self.activity_insight_cooldown:
            print(f"Activity insight for {activity['app_names']} is still valid")
            return
          break
    
    if self.is_ai_processing_locked:
      print(f"AI is already processing data, skipping activity insight for {self.data['apps'][pid]['app_name']}")
      return
    self.is_ai_processing_locked = True

    # Build the data to be sent to the AI
    activity_apps = {k: v for k, v in self.data['apps'].items() if k in activity_app_pids}
    include_keys = ['app_name', 'active_time_seconds', 'insight']
    activity_data = [
      {k: v for k, v in app_data.items() if k in include_keys}
      for app_data in activity_apps.values()
    ]

    # Function to set the insight that is returned from the AI
    def set_insight(insight):
      self.is_ai_processing_locked = False
      if insight is None:
        print(f"Insight for {self.data['apps'][pid]['app_name']} is None")
        return

      found = False
      for activity in self.data['activities']:
        if activity_app_names.issubset(activity['app_names']) or activity['app_names'].issubset(activity_app_names):
          activity['insight']['history'].append({
            'app_names': activity['app_names'],
            'insight': {
              'value': activity['insight']['value'],
              'timestamp': activity['insight']['timestamp']
            }
          })
          activity['insight']['value'] = insight
          activity['insight']['timestamp'] = time.time()
          activity['app_names'] = activity_app_names
          found = True
          break

      if not found:
        self.data['activities'].append({
          'app_names': activity_app_names,
          'insight': {
            'value': insight,
            'timestamp': time.time(),
            'history': []
          }
        })

      self.new_activity_insight_event.invoke()

    # In a new thread, call analyze_data with the app_data
    threading.Thread(target=analyze_data, args=("activity_insight", activity_data, set_insight)).start()