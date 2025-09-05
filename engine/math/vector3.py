import numpy as np


class Vector3:
  """
  A 3D vector class for mathematical operations and vector manipulations.
  Attributes:
    x (float): The x-component of the vector.
    y (float): The y-component of the vector.
    z (float): The z-component of the vector.
    magnitude (float): The magnitude (length) of the vector.
    normalized (Vector3): A normalized (unit length) version of the vector.
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
    vec1 = Vector3([1, 2])
    vec2 = Vector3([3, 4])
    result = vec1 + vec2
    print(result)  # Output: X: 4.0 | Y: 6.0
  """
  def __init__(self, array_like):
    if type(array_like) == Vector3:
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
  def z(self):
    return self._vec[2]
  
  @property
  def magnitude(self):
    return np.linalg.norm(self._vec)
  
  @property
  def normalized(self):
    if self.magnitude == 0:
      return Vector3.zero
    return Vector3(self._vec / self.magnitude)
  
  # Class methods
  def __getitem__(self, key):
    return self._vec[key]
  
  # for negative of vector
  def __neg__(self):
    return Vector3(-self._vec)

  def __add__(self, other):
    if type(other) != Vector3:
      other = Vector3(other)
    return Vector3(self._vec + other._vec)
  
  def __sub__(self, other):
    if type(other) != Vector3:
      other = Vector3(other)
    return Vector3(self._vec - other._vec)
  
  def __mul__(self, other):
    return Vector3(self._vec * other)
  
  def __rmul__(self, other):
    return Vector3(self._vec * other)
  
  def __truediv__(self, other):
    return Vector3(self._vec / other)
  
  def __eq__(self, other):
    if type(other) != Vector3:
      return False
    return np.array_equal(self._vec, other._vec)
  
  def __str__(self):
    x, y, z = self._vec
    x = round(x, 1)
    y = round(y, 1)
    z = round(z, 1)
    return f"X: {x} | Y:{y} | Z:{z}"
  
  def __repr__(self):
    x, y, z = self._vec
    x = round(x, 1)
    y = round(y, 1)
    z = round(z, 1)
    return f"Vector3({x}, {y}, {z})"
  
  def equals(self, other):
    return self == other
  
  def normalize(self):
    self._vec = self.normalized._vec

  def astype(self, dtype):
    return Vector3(self._vec.astype(dtype))

  # Types variables
  int = np.int32
  float = np.float32

  # Static methods
  @staticmethod
  def random() -> "Vector3":
    """
    Generates a random 3D vector with components in the range [-1, 1] and returns its normalized form.

    Returns:
      Vector3: A normalized 3D vector with random components.
    """
    return Vector3(np.random.rand(3) * 2 - 1).normalized

  @staticmethod
  def angle(vec1: "Vector3", vec2: "Vector3") -> float:
    """
    Calculate the angle (in radians) between two 3D vectors.

    This function computes the angle between two vectors using the dot product
    and the magnitudes of the vectors. The result is in the range [0, π].

    Args:
      vec1 (Vector3): The first 3D vector.
      vec2 (Vector3): The second 3D vector.

    Returns:
      float: The angle in radians between the two vectors.
    """
    return np.arccos(Vector3.dot(vec1, vec2) / (vec1.magnitude * vec2.magnitude))
  
  @staticmethod
  def distance(vec1: "Vector3", vec2: "Vector3") -> float:
    """
    Calculate the Euclidean distance between two 3D vectors.

    Args:
      vec1 (Vector3): The first vector, an instance of the Vector3 class.
      vec2 (Vector3): The second vector, an instance of the Vector3 class.

    Returns:
      float: The Euclidean distance between vec1 and vec2.
    """
    return np.linalg.norm(vec1._vec - vec2._vec)
  
  @staticmethod
  def dot(vec1: "Vector3", vec2: "Vector3") -> float:
    """
    Compute the dot product of two 3D vectors.

    Args:
      vec1 (Vector3): The first vector.
      vec2 (Vector3): The second vector.

    Returns:
      float: The dot product of the two vectors.
    """
    return np.dot(vec1._vec, vec2._vec)

  @staticmethod
  def cross(vec1: "Vector3", vec2: "Vector3") -> "Vector3":
    """
    Compute the cross product of two 3D vectors.

    Args:
      vec1 (Vector3): The first vector.
      vec2 (Vector3): The second vector.

    Returns:
      Vector3: The cross product of the two vectors.
    """
    return Vector3(np.cross(vec1._vec, vec2._vec))

  @staticmethod
  def reflect(vec: "Vector3", normal: "Vector3") -> "Vector3":
    """
    Reflects a vector off a surface with the given normal.

    This function calculates the reflection of a vector `vec` 
    when it hits a surface with a specified normal vector `normal`.
    The reflection is computed using the formula:
      R = vec - 2 * (vec • normal) * normal
    where `•` denotes the dot product.

    Args:
      vec (Vector3): The vector to be reflected.
      normal (Vector3): The normal vector of the surface.

    Returns:
      Vector3: The reflected vector.
    """
    return vec - 2 * Vector3.dot(vec, normal) * normal
  
  @staticmethod
  def clamp_magnitude(vec: "Vector3", max_magnitude: float) -> "Vector3":
    """
    Clamps the magnitude of a 3D vector to a specified maximum value.

    If the vector's magnitude exceeds the given maximum, the vector is scaled
    down to have the specified magnitude while maintaining its direction.
    Otherwise, the vector remains unchanged.

    Args:
      vec (Vector3): The 3D vector to clamp.
      max_magnitude (float): The maximum allowable magnitude for the vector.

    Returns:
      Vector3: A new vector with its magnitude clamped to the specified maximum.
    """
    if vec.magnitude > max_magnitude:
      return vec.normalized * max_magnitude
    return vec
  
  @staticmethod
  def rotate(point: "Vector3", origin: "Vector3", axis: "Vector3", angle: float) -> "Vector3":
    """
    Rotates a point around a given axis by a specified angle.

    Args:
      point (Vector3): The point to be rotated.
      origin (Vector3): The origin point around which to rotate.
      axis (Vector3): The axis of rotation.
      angle (float): The angle of rotation in radians.

    Returns:
      Vector3: The rotated point.
    """
    # Normalize the axis
    axis = axis.normalized
    # Calculate the rotation matrix
    cos_angle = np.cos(angle)
    sin_angle = np.sin(angle)
    ux, uy, uz = axis.x, axis.y, axis.z

    rotation_matrix = np.array([
        [cos_angle + ux**2 * (1 - cos_angle), ux * uy * (1 - cos_angle) - uz * sin_angle, ux * uz * (1 - cos_angle) + uy * sin_angle],
        [uy * ux * (1 - cos_angle) + uz * sin_angle, cos_angle + uy**2 * (1 - cos_angle), uy * uz * (1 - cos_angle) - ux * sin_angle],
        [uz * ux * (1 - cos_angle) - uy * sin_angle, uz * uy * (1 - cos_angle) + ux * sin_angle, cos_angle + uz**2 * (1 - cos_angle)]
    ])

    # Translate point to origin
    translated_point = point - origin
    # Rotate the point
    rotated_point = rotation_matrix @ translated_point._vec
    # Translate back to original position
    return Vector3(rotated_point + origin._vec)
  
  up = None
  down = None
  left = None
  right = None
  forward = None
  back = None
  zero = None

# Static variables
# TODO: Change these to be relative to the camera
Vector3.up = Vector3([0, -1, 0])
Vector3.down = Vector3([0, 1, 0])
Vector3.left = Vector3([-1, 0, 0])
Vector3.right = Vector3([1, 0, 0])
Vector3.forward = Vector3([0, 0, 1])
Vector3.back = Vector3([0, 0, -1])
Vector3.zero = Vector3([0, 0, 0])