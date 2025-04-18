import math

from engine import Environment, Component
from engine.math import Vector2


class Movement(Component):
  def __init__(self, **kwargs):
    self.proxity_limit = 300
    self.normal_move_speed = 50
    self.asleep_move_speed = 10

    self.move_mode = ''
    self.default_move_mode = 'idle'
    self.default_drag = self.drag if hasattr(self, 'drag') else 0.05
    self.default_gravity = self.use_gravity if hasattr(self, 'use_gravity') else True
    super().__init__(**kwargs)

  def set_move_mode(self, mode):
    self.move_mode = mode

    move_modes = {
      'sleep': self.sleep_drift,
      'idle': self.reset,
    }

    if mode in move_modes:
      move_modes[mode]()
    else:
      self.reset()

  def update(self):
    super().update()
    # Depending on the movement mode, get the new desired display position
    if self.move_mode != 'hold': # Always avoid the cursor unless explicitly told not to
      self.cursor_avoidance()

  ######################################################
  ################## Movement Actions ##################
  ######################################################

  # Apply a force to the object to keep it away from the cursor
  def cursor_avoidance(self):
    current_position = self.transform.position

    # vector between mouse and display center
    distance = Vector2([
      (current_position.x + self.transform.width // 2) - Environment.mouse_position.x,
      (current_position.y + self.transform.height // 2) - Environment.mouse_position.y
    ])

    # Move the display window based on the mouse position
    force_factor = max(1.0 - distance.magnitude / self.proxity_limit, 0)
    force = math.trunc(self.normal_move_speed * force_factor)
    self.apply_force(distance.normalized * force)
  
  def reset(self):
    self.use_gravity = self.default_gravity
    self.drag = self.default_drag

  # Disable gravity and drag and then apply a small force in a random direction
  def sleep_drift(self):
    self.use_gravity = False
    self.drag = 0.01
    self.apply_force(Vector2.random() * self.asleep_move_speed)
