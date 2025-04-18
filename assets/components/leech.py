from engine import Environment, Component
from engine.math import Vector2


class Leech(Component):
  def __init__(self, **kwargs):
    self.window_name = kwargs.get('window_name', None)
    self.auto_size = kwargs.get('auto_size', False)
    self.offset_position = kwargs.get('offset_position', Vector2([0, 0]))

    self.desired_size = None
    self.attached_app = None
    self.is_leech_attached = False
    self.lerp_speed = 0.005
    super().__init__(**kwargs)

  def start(self):
    super().start()
    self.desired_size = self.transform.size
    self.transform.size = (0, 0)
    self.transform.position = (0, 0)
    self.search()
  
  def update(self):
    super().update()
    # If the window is not active, search for it
    if not self.is_leech_attached:
      self.search()
      return
    # Check if the window is still open
    if self.attached_app.pid not in Environment.applications:
      print(f'Window {self.window_name} has been lost')
      self.transform.size = (0, 0)
      self.transform.position = (0, 0)
      self.window_pid = None
      self.is_leech_attached = False
      return
    
    # Lerp to position of the window
    self.transform.position = self.transform.position + ((self.attached_app.position + self.offset_position) - self.transform.position) * self.lerp_speed * self.delta_time
    if self.auto_size: self.transform.size = self.attached_app.size

  def search(self):
    # Look up window name in Environment.applications
    for app in Environment.applications.values():
      if app.name == self.window_name:
        # If it exists, return the application
        print(f'Found application {app.name} with pid {app.pid} and title {app.title}')
        self.attached_app = app

        # Update object size and position to match the window
        self.transform.position = app.position + self.offset_position
        if self.auto_size:
          self.transform.size = app.size
        else:
          self.transform.size = self.desired_size
        self.is_leech_attached = True
        return