from enum import Enum
import numpy as np

###################################
############# Vector2 #############
###################################

class Vector2:
  def __init__(self, array_like):
    if type(array_like) == Vector2:
      array_like = array_like._vec
    self._vec = np.array(array_like)
  
  # Properties
  @property
  def x(self):
    return self._vec[0]
  
  @property
  def y(self):
    return self._vec[1]
  
  @property
  def magnitude(self):
    return np.linalg.norm(self._vec)
  
  @property
  def normalized(self):
    if self.magnitude == 0:
      return Vector2.zero
    return Vector2(self._vec / self.magnitude)
  
  # Class methods
  def __getitem__(self, key):
    return self._vec[key]
  
  # for negative of vector
  def __neg__(self):
    return Vector2(-self._vec)

  def __add__(self, other):
    return Vector2(self._vec + other._vec)
  
  def __sub__(self, other):
    return Vector2(self._vec - other._vec)
  
  def __mul__(self, other):
    return Vector2(self._vec * other)
  
  def __rmul__(self, other):
    return Vector2(self._vec * other)
  
  def __truediv__(self, other):
    return Vector2(self._vec / other)
  
  def __eq__(self, other):
    if type(other) != Vector2:
      return False
    return np.array_equal(self._vec, other._vec)
  
  def __str__(self):
    x, y = self._vec
    x = round(x, 1)
    y = round(y, 1)
    return f"X: {x} | Y:{y}"
    # return f"Vector2({self._vec})"
  
  def equals(self, other):
    return self == other
  
  def normalize(self):
    self._vec = self.normalized._vec

  def astype(self, dtype):
    return Vector2(self._vec.astype(dtype))

  # Types variables
  int = np.int32
  float = np.float32

  # Static methods
  def random():
    return Vector2(np.random.rand(2) * 2 - 1).normalized

  def angle(vec1, vec2):
    return np.arccos(Vector2.dot(vec1, vec2) / (vec1.magnitude * vec2.magnitude))
  
  def distance(vec1, vec2):
    return np.linalg.norm(vec1._vec - vec2._vec)
  
  def dot(vec1, vec2):
    return np.dot(vec1._vec, vec2._vec)
  
  def reflect(vec, normal):
    return vec - 2 * Vector2.dot(vec, normal) * normal
  
  def clamp_magnitude(vec, max_magnitude):
    if vec.magnitude > max_magnitude:
      return vec.normalized * max_magnitude
    return vec

# Static variables
Vector2.up = Vector2([0, -1])
Vector2.down = Vector2([0, 1])
Vector2.left = Vector2([-1, 0])
Vector2.right = Vector2([1, 0])
Vector2.zero = Vector2([0, 0])

###################################
########## Util Functions #########
###################################

def away_from_zero(x):
  return int(x // 1 + 2 ** (x > 0) - 1)

###################################
############# Enums ###############
###################################

class Side(Enum):
  TOP = 0
  RIGHT = 1
  BOTTOM = 2
  LEFT = 3
