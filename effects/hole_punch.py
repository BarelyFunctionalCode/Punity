from objects.object import Object
from objects.hole import Hole
from objects.screen_chunk import ScreenChunk

from components.rigidbody import Rigidbody

from environment import Instance as environment

class ScreenChunkRigidbody(ScreenChunk, Rigidbody):
  def __init__(self, parent, polygon, x, y, lifetime=-1, collision_enabled=True):
    super().__init__(parent, polygon, x, y, lifetime, False)
    self.collision_enabled = collision_enabled

  def start(self):
    super().start() if hasattr(super(), 'start') else None
    self.gravity_modifier = 0.5
    self.bounciness = 0.2

  def update(self):
    super().update() if hasattr(super(), 'update') else None



class HolePunch(Object):
  def __init__(self, parent, hole_polygon, x, y, lifetime=-1, collision_enabled=True):
    self.hole_polygon = hole_polygon
    self.lifetime = lifetime
    self.collision_enabled = collision_enabled
    super().__init__(parent, 'hole_punch', 0, 0, x, y,True)


  def start(self):
    super().start() if hasattr(super(), 'start') else None
    # Create the hole object
    self.hole = Hole(self.root, self.hole_polygon, self.transform.position.x, self.transform.position.y, self.lifetime)
    # Create the screen chunk object
    self.screen_chunk = ScreenChunkRigidbody(self.root, self.hole_polygon, self.transform.position.x, self.transform.position.y, self.lifetime if self.collision_enabled else -1, self.collision_enabled)


  def update(self):
    super().update() if hasattr(super(), 'update') else None
    if self.screen_chunk and self.screen_chunk.transform.position.y > environment.height:
      self.screen_chunk.destroy()
      self.screen_chunk = None

    if self.screen_chunk and self.screen_chunk.root == None:
      self.screen_chunk = None

    if self.hole and self.hole.root == None:
      self.hole = None

    if self.screen_chunk == None and self.hole == None:
      self.destroy()
      return