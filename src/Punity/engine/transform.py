from typing import TYPE_CHECKING

from .math import Vector2
if TYPE_CHECKING:
  from .object import Object


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

  def __init__(self, object, x, y, width, height):
    self.object: "Object" = object
    self._position = Vector2([x, y])
    self._local_position = Vector2.zero
    self._last_position = Vector2(self.position)
    self._desired_position = Vector2(self.position)
    self._desired_local_position = None
    self._did_move_this_frame = True
    self._width = width
    self._height = height

  @property
  def position(self) -> Vector2:
    """
    Gets the current position of the object.

    Returns:
      Vector2: The current position as a 2D vector.
    """
    return self._position

  @property
  def local_position(self) -> Vector2:
    """
    Gets the local position of the object relative to its parent.

    Returns:
      Vector2: The local position as a 2D vector.
    """
    return self._local_position

  @position.setter
  def position(self, new_position: Vector2 | tuple | list):
    if not isinstance(new_position, Vector2):
      new_position = Vector2(new_position)
    self._desired_position = new_position
    if Vector2.distance(self._desired_position, self._position) > 0:
      self._did_move_this_frame = True

  @local_position.setter
  def local_position(self, new_local_position: Vector2 | tuple | list):
    if not isinstance(new_local_position, Vector2):
      new_local_position = Vector2(new_local_position)
    self._desired_local_position = new_local_position
    if Vector2.distance(self._desired_local_position, self._local_position) > 0:
      self._did_move_this_frame = True

  def _resolve_position_update(self):
    if self._did_move_this_frame:
      parent_position = Vector2([0, 0])
      if self.object.parent is not None and self.object.parent.transform is not None:
        parent_position = self.object.parent.transform.position
      self._last_position = Vector2(self.position)

      if self._desired_local_position is not None:
        self._position = self._desired_local_position + parent_position

      if self._desired_position is not None:
        self._position = Vector2(self._desired_position)

      self._local_position = self._position - parent_position

      self._desired_local_position = None
      self._desired_position = None
      self._did_move_this_frame = False
      self.object.update_visuals()

      return self.position - self._last_position
    return Vector2.zero

  @property
  def direction(self) -> Vector2:
    """
    Calculate and return the direction vector based on the difference 
    between the current position and the last position.

    Returns:
      Vector2: A vector representing the direction of movement.
    """
    return self.position - self._last_position

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
    self.object.update_visuals()
  
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
    self.object.update_visuals()
  
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
    self.object.update_visuals()

  @property
  def rect(self) -> tuple:
    """
    Gets the rectangle representing the object's position and size.

    Returns:
      tuple: A tuple (x, y, width, height) representing the object's rectangle.
    """
    return (self.position.x, self.position.y, self._width, self._height)