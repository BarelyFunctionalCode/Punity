import math

from ..utils import Vector2
from ..environment import Instance as environment

class Movement:
  def __init__(self):
    super().__init__()
    self.proxity_limit = 300
    self.normal_move_speed = 100
    self.asleep_move_speed = 2

    self.move_mode = ''

  def set_move_mode(self, mode):
    print(f'Set move mode to {mode}')
    self.move_mode = mode

  def check_for_movement(self):
    # Depending on the movement mode, get the new desired display position
    new_movement = Vector2.zero
    if self.move_mode != 'hold': # Always avoid the cursor unless explicitly told not to
      new_movement = self.cursor_avoidance()
    if self.move_mode == 'sleep' and new_movement == Vector2.zero:
      new_movement = self.sleep_drift()

    return new_movement
    
  def update(self):
    super().update() if hasattr(super(), 'update') else None
    
    # Update the display window position if needed
    new_movement = self.check_for_movement()
    if not new_movement == Vector2.zero:
      self.transform.position = self.transform.position + new_movement


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
    move_factor = max(1.0 - distance.magnitude / self.proxity_limit, 0)
    move_amount = math.trunc(self.normal_move_speed * move_factor)
    return distance.normalized * move_amount
  

  def sleep_drift(self):
    # Determine if it is already moving and what direction
    current_direction = (self.transform.position - self.transform.last_position).normalized

    # Randomly select a direction to drift in
    if current_direction == Vector2.zero:
      current_direction = Vector2.random()

    return current_direction * self.asleep_move_speed

  def on_collision(self, col_normal, col_vec, other_object):
    super().on_collision(col_normal, col_vec, other_object) if hasattr(super(), 'on_collision') else None
    
    if self.move_mode == 'sleep':
      new_direction = Vector2.reflect(col_vec, col_normal)

      collision_response = new_direction * self.asleep_move_speed
      self.transform.position = self.transform.position + collision_response
