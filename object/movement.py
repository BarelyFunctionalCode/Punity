import math

from utils import Vector2
from environment import Instance as environment

class Movement:
  def __init__(self):
    super().__init__()
    self.proxity_limit = 300
    self.normal_move_speed = 50
    self.asleep_move_speed = 10

    self.move_mode = ''

  def set_move_mode(self, mode):
    self.move_mode = mode

    if mode == 'sleep':
      self.sleep_drift()

  def update(self):
    super().update() if hasattr(super(), 'update') else None
    # Depending on the movement mode, get the new desired display position
    if self.move_mode != 'hold': # Always avoid the cursor unless explicitly told not to
      self.cursor_avoidance()

  ######################################################
  ################## Movement Actions ##################
  ######################################################

  def cursor_avoidance(self):
    current_position = self.transform.position

    # vector between mouse and display center
    distance = Vector2([
      (current_position.x + self.transform.width // 2) - environment.mouse_position.x,
      (current_position.y + self.transform.height // 2) - environment.mouse_position.y
    ])

    # Move the display window based on the mouse position
    force_factor = max(1.0 - distance.magnitude / self.proxity_limit, 0)
    force = math.trunc(self.normal_move_speed * force_factor)
    self.apply_force(distance.normalized * force)
  

  def sleep_drift(self):
    # Disable gravity and drag and then apply a small force in a random direction
    self.use_gravity = False
    self.drag = 0.01
    self.apply_force(Vector2.random() * self.asleep_move_speed)
