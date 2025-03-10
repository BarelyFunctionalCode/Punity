import time
import numpy as np

from components.transform import Transform
from utils import Vector2

from environment import Instance as environment

class Object:
  def __init__(self, name, root, is_static=True):
    self.name = name
    self.root = root
    self.is_static = is_static
    self.collision_enabled = False
    self.collision_ignore_list = []
    self.transform = Transform(self)
    super().__init__()

    self.last_update_time = time.time()

    environment.objects = np.append(environment.objects, self)
    self.start()
    self._update()

  @property
  def delta_time(self):
    return (time.time() - self.last_update_time) * 1000
    
  def _update(self):
    if self.root == None: return
    self.update()
    if self.root == None: return
    if not self.is_static:
      for obj in environment.objects:
        if obj == self: continue
        col_normal = self._collision_check(obj)
        if col_normal != None:
          self.on_collision(col_normal, obj)
          if not obj.is_static:
            obj.on_collision(-col_normal, self)

      new_position = self.transform.position.astype(Vector2.int)
      self.root.update_idletasks()
      self.root.geometry(f"{self.transform.width}x{self.transform.height}+{new_position.x}+{new_position.y}")
    self.last_update_time = time.time()
    self.root.after(10, self._update)

  def start(self):
    super().start() if hasattr(super(), 'start') else None

  def update(self):
    super().update() if hasattr(super(), 'update') else None

  def destroy(self):
    self.root.destroy()
    self.root = None
    environment.objects = np.delete(environment.objects, np.where(environment.objects == self))
    
  def _collision_check(self, other):
    if not self.collision_enabled or not other.collision_enabled: return None
    if other.name in self.collision_ignore_list: return None
    if self.name in other.collision_ignore_list: return None
    did_collide = False
    if self.transform.position.x < other.transform.position.x + other.transform.width and \
       self.transform.position.x + self.transform.width > other.transform.position.x and \
       self.transform.position.y < other.transform.position.y + other.transform.height and \
       self.transform.position.y + self.transform.height > other.transform.position.y:
      did_collide = True
    
    if did_collide:
      # Get Collision vector
      collision_relative_position = self.transform.position - other.transform.position

      possible_collisions = np.array([
        # Top side
        collision_relative_position.y + self.transform.height,
        # Left side
        collision_relative_position.x + self.transform.width,
        # Bottom side
        collision_relative_position.y - other.transform.height,
        # Right side
        collision_relative_position.x - other.transform.width,
      ])

      directions = np.array([
        Vector2.up,
        Vector2.left,
        Vector2.down,
        Vector2.right,
      ])

      # Get the normal of the collision
      return directions[np.argmin(np.abs(possible_collisions))]
    return None

  def on_collision(self, col_normal, other_object):
    col_vec = self.transform.position - self.transform.last_position

    collision_response = col_normal * col_vec.magnitude
    # print(f"Base Collision: {col_normal} with {other_object.name}; {self.transform.position} {other_object.transform.position}") 
    # print(f"Base Collision: {col_normal} with {other_object.name}; Response: {collision_response} {self.transform.position} {other_object.transform.position}") 
    self.transform.position = self.transform.position + collision_response

    super().on_collision(col_normal, col_vec, other_object) if hasattr(super(), 'on_collision') else None
