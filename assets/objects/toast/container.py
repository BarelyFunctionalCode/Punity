import numpy as np

from engine import Environment
from engine import Object

class ToastContainer(Object):
  def __init__(self, parent, x, y):
    self.move_speed = 2

    super().__init__(parent, "toast_container", 0, 0, x, y, True)
    self.collision_enabled = False

  def update(self):
    super().update()

    flipped_children = np.array(self.children)[::-1]
    if len(flipped_children) > 0:
      desired_y = Environment.y + 5
      for child in flipped_children:

        # Move Toast to the right till it is fully on screen
        current_position = child.transform.position
        if current_position.x < 0:
          child.transform.position = [current_position.x + self.move_speed * self.delta_time, current_position.y]
        elif current_position.x > 0:
          child.transform.position = [0, current_position.y]

        # Move Toast up/down to form a stack
        current_position = child.transform.position
        y_distance = abs(current_position.y - desired_y) / desired_y
        if current_position.y < desired_y:
          child.transform.position = [current_position.x, current_position.y + y_distance * self.move_speed * self.delta_time]
        elif current_position.y > desired_y:
          child.transform.position = [current_position.x, current_position.y - y_distance * self.move_speed * self.delta_time]
        elif y_distance < 5:
          child.transform.position = [current_position.x, desired_y]

        desired_y += child.transform.height + 5