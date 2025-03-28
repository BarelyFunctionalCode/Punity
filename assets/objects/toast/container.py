from engine import Object


class ToastContainer(Object):
  def __init__(self, parent, x, y):
    self.move_speed = 1

    super().__init__(parent, "toast_container", 0, 0, x, y, True)
    self.collision_enabled = False

  def update(self):
    super().update()

    if len(self.children) > 0:
      for child in self.children:
        current_position = child.transform.position
        if current_position.x < 0:
          child.transform.position = [current_position.x + self.move_speed * self.delta_time, current_position.y]