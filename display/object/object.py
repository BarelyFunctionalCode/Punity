import numpy as np

from .transform import Transform
from ..utils import Vector2

from ..environment import Instance as environment

class Object:
  def __init__(self, name, root, is_static=True):
    self.name = name
    self.root = root
    self.is_static = is_static
    self.transform = Transform(self)
    super().__init__()

    environment.objects = np.append(environment.objects, self)
    self._update()
    
  def _update(self):
    if self.root == None: return
    self.update()
    if not self.is_static:
      for obj in environment.objects:
        if obj == self: continue
        col_normal = self._collision_check(obj)
        if col_normal != None:
          self.on_collision(col_normal, obj)

    new_position = self.transform.position.astype(Vector2.int)
    self.root.update_idletasks()
    self.root.geometry(f"{self.transform.width}x{self.transform.height}+{new_position.x}+{new_position.y}")
    self.root.after(10, self._update)

  def update(self):
    super().update() if hasattr(super(), 'update') else None

  def _collision_check(self, other):
    did_collide = False
    if self.transform.position.x < other.transform.position.x + other.transform.width and \
       self.transform.position.x + self.transform.width > other.transform.position.x and \
       self.transform.position.y < other.transform.position.y + other.transform.height and \
       self.transform.position.y + self.transform.height > other.transform.position.y:
      did_collide = True
    
    if did_collide:
      # Get Collision vector
      collision_vector = self.transform.position - other.transform.position

      collision_factors = np.array([
        # Top side
        collision_vector.y + self.transform.height,
        # Left side
        collision_vector.x + self.transform.width,
        # Bottom side
        collision_vector.y - other.transform.height,
        # Right side
        collision_vector.x - other.transform.width,
      ])

      directions = np.array([
        Vector2.up,
        Vector2.left,
        Vector2.down,
        Vector2.right,
      ])

      # Get the normal of the collision
      return directions[np.argmin(np.abs(collision_factors))]
    return None

  def on_collision(self, col_normal, other_object):
    col_vec = self.transform.position - self.transform.last_position

    collision_response = col_normal * col_vec.magnitude
    print(f"Base Collision: {col_normal} with {other_object.name}; Response: {collision_response}")
    self.transform.position = self.transform.position + collision_response

    super().on_collision(col_normal, col_vec, other_object) if hasattr(super(), 'on_collision') else None
