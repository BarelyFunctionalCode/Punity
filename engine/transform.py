from engine.math import Vector2


class Transform:
  # Positional information used to update the TK Windows
  def __init__(self, object):
    self.object = object
    self._position = Vector2([self.object.tk_obj.winfo_x(), self.object.tk_obj.winfo_y()])
    self._last_position = Vector2(self._position)
    self.did_move_this_frame = False
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
    self.did_move_this_frame = True
    # print(f"Setting position to {new_position} from {self._last_position}")

  @property
  def direction(self):
    return self._position - self._last_position

  @property
  def width(self):
    return self._width
  
  @width.setter
  def width(self, new_width):
    if not isinstance(new_width, int):
      raise Exception('Width must be an integer')
    self._width = new_width
  
  @property
  def height(self):
    return self._height
  
  @height.setter
  def height(self, new_height):
    if not isinstance(new_height, int):
      raise Exception('Height must be an integer')
    self._height = new_height
  
  @property
  def size(self):
    return Vector2([self._width, self._height])
  
  @size.setter
  def size(self, new_size):
    if not isinstance(new_size, Vector2):
      new_size = Vector2(new_size)
    self._width = int(new_size.x)
    self._height = int(new_size.y)