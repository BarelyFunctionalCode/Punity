import tkinter as tk

from engine import Component, Environment

class BrainFart:
  def __init__(self):
    self.window = tk.Toplevel()
    self.window.title("BrainFart")
    self.window.geometry(f"500x600+0+0")
    self.window.update_idletasks()
    self.window.wm_attributes("-topmost", True)

    self.activity_label = tk.Label(self.window, text="", font=('Courier New', 12), justify='left', anchor='nw')
    self.activity_label.pack(expand=True, fill=tk.BOTH)
  
  def update(self, text):
    self.activity_label.config(text=text)
    self.window.update_idletasks()

class Brain(Component):
  def __init__(self, **kwargs):
    self.data = {
      'apps': {},
    }

    self.last_event_pid = -1
    self.last_event_time = 0
    self.inactivity_timeout = 10000
    self.inactivity_timer = 0

    self.brain_fart = None
    if Environment.dev_mode:
      self.brain_fart = BrainFart()
      self.brain_fart.update("BrainFart Initialized")
    
    super().__init__()

  def start(self):
    super().start()
    Environment.new_input_event.add_listener(self.ingest_input_event)
    

  def update(self):
    super().update()
    
    # Check if the last event was too long ago
    if self.last_event_pid != -1 and self.inactivity_timer > self.inactivity_timeout:
      self.last_event_pid = -1
      self.last_event_time = 0

      if self.brain_fart:
        self.brain_fart.update(self.get_dev_info())
    else:
      self.inactivity_timer += self.delta_time

  def ingest_input_event(self, event_data):
    # Get data that would be given for any input event
    pid = event_data['pid']
    timestamp = event_data['timestamp']
    app_name = Environment.applications[pid].name if pid != -1 else 'Unknown'
    app_title = Environment.applications[pid].title if pid != -1 else 'Unknown'

    # Create entry in data['apps'] dict if it doesn't exist
    if pid not in self.data['apps']:
      self.data['apps'][pid] = {
        'app_name': app_name,
        'raw_text_data': [],
        'clicks': 0,
        'activity_time': 0,
      }
    
    # Update data from relevent input event
    self.data['apps'][pid]['app_title'] =  app_title
    self.data['apps'][pid]['last_active_time'] =  timestamp
    if event_data['type'] == 'keyboard_log':
      self.data['apps'][pid]['raw_text_data'].append(event_data['text'])
    elif event_data['type'] == 'mouse_down':
      self.data['apps'][pid]['clicks'] += 1

    if self.last_event_pid == pid:
      self.data['apps'][pid]['activity_time'] += (timestamp - self.last_event_time)

    self.last_event_pid = pid
    self.last_event_time = timestamp
    self.inactivity_timer = 0


  def get_dev_info(self):
    text = 'App Name | App Title | Activity Ratio\n'
    text += '----------------------\n'
    total_time = 0
    for pid in self.data['apps']:
      total_time += self.data['apps'][pid]['activity_time']
    for pid in self.data['apps']:
      ratio = self.data['apps'][pid]['activity_time'] / total_time
      text += f"{self.data['apps'][pid]['app_name']} | {self.data['apps'][pid]['app_title']} | {ratio:.2%}\n"
    text += f"----------------------\nTotal Time: {total_time}\n\n"

    for pid in self.data['apps']:
      if len(self.data['apps'][pid]['raw_text_data']) > 0:
        text += f"Raw Text Data for {self.data['apps'][pid]['app_name']}:\n"
        for line in self.data['apps'][pid]['raw_text_data']:
          text += f"{line}\n"
        text += "\n"

    return text