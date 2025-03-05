from ..utils import Vector2

class Transform:
  def __init__(self, object):
    self.object = object
    self._last_position = Vector2(self.position)

  @property
  def position(self):
    return Vector2([self.object.root.winfo_x(), self.object.root.winfo_y()])

  @position.setter
  def position(self, new_position):
    self.object.root.update_idletasks()
    self._last_position = Vector2(self.position)
    self.object.root.geometry(f"{self.width}x{self.height}+{new_position.x}+{new_position.y}")


  @property
  def last_position(self):
    return self._last_position


  @property
  def width(self):
    return self.object.root.winfo_width()
  

  @property
  def height(self):
    return self.object.root.winfo_height()