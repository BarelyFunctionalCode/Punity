import numpy as np
import math

from ..environment import Instance as environment

def away_from_zero(x):
  return int(x // 1 + 2 ** (x > 0) - 1)

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

  def check_for_movement(self, transform):
    # Depending on the movement mode, get the new desired display position
    new_movement = np.zeros(2)
    if self.move_mode != 'hold': # Always avoid the cursor unless explicitly told not to
      new_movement = self.cursor_avoidance(transform)
    if self.move_mode == 'sleep' and np.array_equal(new_movement, np.zeros(2)):
      new_movement = self.sleep_drift(transform)

    return new_movement
    
  def update(self):
    super().update() if hasattr(super(), 'update') else None
    
    # Update the display window position if needed
    new_movement = self.check_for_movement(self.transform)
    if not np.array_equal(new_movement, np.zeros(2)):
      self.transform.position = self.transform.position + new_movement


  ######################################################
  ################## Movement Actions ##################
  ######################################################

  def cursor_avoidance(self, transform):
    current_position = transform.position

    # vector between mouse and display center
    distance = np.array([
      (current_position[0] + transform.width // 2) - environment.mouse_position[0],
      (current_position[1] + transform.height // 2) - environment.mouse_position[1]
    ])
    magnitude = np.linalg.norm(distance)
    direction = distance / magnitude

    # Move the display window based on the mouse position
    move_factor = max(1.0 - magnitude / self.proxity_limit, 0)
    move_amount = math.trunc(self.normal_move_speed * move_factor)
    return (direction * move_amount).astype(np.int32)
  


  def sleep_drift(self, transform):
    last_movement = transform.position - transform.last_position
    current_direction = last_movement
    if not np.array_equal(last_movement, np.zeros(2)):
      current_direction = last_movement / np.linalg.norm(last_movement)
    else:
      # Randomly select a direction to drift in
      current_direction = np.random.rand(2) * 2 - 1
      current_direction = current_direction / np.linalg.norm(current_direction)

    print(f'Current direction: {current_direction}')

    return (current_direction * self.asleep_move_speed).astype(np.int32)


    