import numpy as np


class Vector2:
  """
  A 2D vector class for mathematical operations and vector manipulations.
  Attributes:
    x (float): The x-component of the vector.
    y (float): The y-component of the vector.
    magnitude (float): The magnitude (length) of the vector.
    normalized (Vector2): A normalized (unit length) version of the vector.
  Methods:
    equals(other): Checks if two vectors are equal (alias for __eq__).
    normalize(): Normalizes the vector in place.
    astype(dtype): Returns a new vector with components cast to the specified data type.
  Class Variables:
    int: Data type for integer components (np.int32).
    float: Data type for floating-point components (np.float32).
  Static Methods:
    random(): Generates a random normalized vector.
    angle(vec1, vec2): Computes the angle (in radians) between two vectors.
    distance(vec1, vec2): Computes the Euclidean distance between two vectors.
    dot(vec1, vec2): Computes the dot product of two vectors.
    reflect(vec, normal): Reflects a vector around a given normal vector.
    clamp_magnitude(vec, max_magnitude): Clamps the magnitude of a vector to a maximum value.
  Static Variables:
    up: A unit vector pointing upwards (0, -1).
    down: A unit vector pointing downwards (0, 1).
    left: A unit vector pointing left (-1, 0).
    right: A unit vector pointing right (1, 0).
    zero: A zero vector (0, 0).
  Usage:
    vec1 = Vector2([1, 2])
    vec2 = Vector2([3, 4])
    result = vec1 + vec2
    print(result)  # Output: X: 4.0 | Y: 6.0
  """
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
    if type(other) != Vector2:
      other = Vector2(other)
    return Vector2(self._vec + other._vec)
  
  def __sub__(self, other):
    if type(other) != Vector2:
      other = Vector2(other)
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
  @staticmethod
  def random() -> "Vector2":
    """
    Generates a random 2D vector with components in the range [-1, 1] and returns its normalized form.

    Returns:
      Vector2: A normalized 2D vector with random components.
    """
    return Vector2(np.random.rand(2) * 2 - 1).normalized

  @staticmethod
  def angle(vec1: "Vector2", vec2: "Vector2") -> float:
    """
    Calculate the angle (in radians) between two 2D vectors.

    This function computes the angle between two vectors using the dot product
    and the magnitudes of the vectors. The result is in the range [0, π].

    Args:
      vec1 (Vector2): The first 2D vector.
      vec2 (Vector2): The second 2D vector.

    Returns:
      float: The angle in radians between the two vectors.
    """
    return np.arccos(Vector2.dot(vec1, vec2) / (vec1.magnitude * vec2.magnitude))
  
  @staticmethod
  def distance(vec1: "Vector2", vec2: "Vector2") -> float:
    """
    Calculate the Euclidean distance between two 2D vectors.

    Args:
      vec1 (Vector2): The first vector, an instance of the Vector2 class.
      vec2 (Vector2): The second vector, an instance of the Vector2 class.

    Returns:
      float: The Euclidean distance between vec1 and vec2.
    """
    return np.linalg.norm(vec1._vec - vec2._vec)
  
  @staticmethod
  def dot(vec1: "Vector2", vec2: "Vector2") -> float:
    """
    Compute the dot product of two 2D vectors.

    Args:
      vec1 (Vector2): The first vector.
      vec2 (Vector2): The second vector.

    Returns:
      float: The dot product of the two vectors.
    """
    return np.dot(vec1._vec, vec2._vec)
  
  @staticmethod
  def reflect(vec: "Vector2", normal: "Vector2") -> "Vector2":
    """
    Reflects a vector off a surface with the given normal.

    This function calculates the reflection of a vector `vec` 
    when it hits a surface with a specified normal vector `normal`.
    The reflection is computed using the formula:
      R = vec - 2 * (vec • normal) * normal
    where `•` denotes the dot product.

    Args:
      vec (Vector2): The vector to be reflected.
      normal (Vector2): The normal vector of the surface.

    Returns:
      Vector2: The reflected vector.
    """
    return vec - 2 * Vector2.dot(vec, normal) * normal
  
  @staticmethod
  def clamp_magnitude(vec: "Vector2", max_magnitude: float) -> "Vector2":
    """
    Clamps the magnitude of a 2D vector to a specified maximum value.

    If the vector's magnitude exceeds the given maximum, the vector is scaled
    down to have the specified magnitude while maintaining its direction.
    Otherwise, the vector remains unchanged.

    Args:
      vec (Vector2): The 2D vector to clamp.
      max_magnitude (float): The maximum allowable magnitude for the vector.

    Returns:
      Vector2: A new vector with its magnitude clamped to the specified maximum.
    """
    if vec.magnitude > max_magnitude:
      return vec.normalized * max_magnitude
    return vec
  
  up = None
  down = None
  left = None
  right = None
  zero = None

# Static variables
Vector2.up = Vector2([0, -1])
Vector2.down = Vector2([0, 1])
Vector2.left = Vector2([-1, 0])
Vector2.right = Vector2([1, 0])
Vector2.zero = Vector2([0, 0])