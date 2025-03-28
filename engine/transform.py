from engine.math import Vector2


class Transform:
  # Positional information used to update the TK Windows
  def __init__(self, object):
    self.object = object
    self._position = Vector2([self.object.tk_obj.winfo_x(), self.object.tk_obj.winfo_y()])
    self._last_position = Vector2(self._position)
    self._width = self.object.tk_obj.winfo_width()
    self._height = self.object.tk_obj.winfo_height()

  @property
  def position(self):
    return self._position

  @position.setter
  def position(self, new_position):
    if not isinstance(new_position, Vector2):
      new_position = Vector2(new_position)
    self._last_position = Vector2(self.position)
    self._position = new_position
    # print(f"Setting position to {new_position} from {self._last_position}")

  @property
  def last_position(self):
    return self._last_position

  @property
  def width(self):
    return self._width
  
  @property
  def height(self):
    return self._height
  
  @property
  def size(self):
    return Vector2([self._width, self._height])