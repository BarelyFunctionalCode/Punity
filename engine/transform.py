from engine.math import Vector2

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from engine import Object


class Transform:
  """
  The Transform class represents the spatial properties of an object, including
  its position, size, and movement direction. It provides methods and properties
  to manipulate and retrieve these attributes.
  Attributes:
    object (Object): The object associated with this transform.
  Properties:
    position (Vector2): Gets or sets the current position of the object.
    direction (Vector2): Gets the direction vector based on the difference 
      between the current and last positions.
    width (int): Gets or sets the width of the object.
    height (int): Gets or sets the height of the object.
    size (Vector2): Gets or sets the size of the object as a 2D vector.
  """

  def __init__(self, object):
    self.object: "Object" = object
    self._position = Vector2([self.object.tk_obj.winfo_x(), self.object.tk_obj.winfo_y()])
    self._last_position = Vector2(self._position)
    self.did_move_this_frame = False
    self._width = self.object.tk_obj.winfo_width()
    self._height = self.object.tk_obj.winfo_height()

  @property
  def position(self) -> Vector2:
    """
    Gets the current position of the object.

    Returns:
      Vector2: The current position as a 2D vector.
    """
    return self._position

  @position.setter
  def position(self, new_position: Vector2 | tuple | list):
    if not isinstance(new_position, Vector2):
      new_position = Vector2(new_position)
    self._last_position = Vector2(self.position)
    self._position = new_position
    self.did_move_this_frame = True

  @property
  def direction(self) -> Vector2:
    """
    Calculate and return the direction vector based on the difference 
    between the current position and the last position.

    Returns:
      Vector2: A vector representing the direction of movement.
    """
    return self._position - self._last_position

  @property
  def width(self) -> int:
    """
    Get the width of the object.

    Returns:
      int: The width of the object.
    """
    return self._width
  
  @width.setter
  def width(self, new_width: int):
    if not isinstance(new_width, int):
      raise Exception('Width must be an integer')
    self._width = new_width
  
  @property
  def height(self) -> int:
    """
    Gets the height of the object.

    Returns:
      int: The height of the object.
    """
    return self._height
  
  @height.setter
  def height(self, new_height: int):
    if not isinstance(new_height, int):
      raise Exception('Height must be an integer')
    self._height = new_height
  
  @property
  def size(self) -> Vector2:
    """
    Returns the size of the object as a Vector2 instance.

    Returns:
      Vector2: The size of the object as a 2D vector.
    """
    return Vector2([self._width, self._height])
  
  @size.setter
  def size(self, new_size: Vector2 | tuple | list):
    if not isinstance(new_size, Vector2):
      new_size = Vector2(new_size)
    self._width = int(new_size.x)
    self._height = int(new_size.y)