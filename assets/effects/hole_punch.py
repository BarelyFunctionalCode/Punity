from engine import Environment
from engine.object import Object

from assets.components.rigidbody import Rigidbody
from assets.objects.hole import Hole
from assets.objects.screen_chunk import ScreenChunk


class ScreenChunkRigidbody(ScreenChunk, Rigidbody):
  def __init__(self, parent, polygon, x, y, lifetime=-1, collision_enabled=True):
    super().__init__(parent, polygon, x, y, lifetime, False)
    self.collision_enabled = collision_enabled
    self.gravity_modifier = 0.5
    self.bounciness = 0.2

  def update(self):
    super().update()


class HolePunch(Object):
  def __init__(self, parent, hole_polygon, x, y, lifetime=-1, collision_enabled=True):
    self.hole_polygon = hole_polygon
    self.lifetime = lifetime
    self.screen_chunk_collision_enabled = collision_enabled
    super().__init__(parent, 'hole_punch', 0, 0, x, y,True)

  def start(self):
    super().start()
    # Create the screen chunk object
    self.screen_chunk = ScreenChunkRigidbody(self, self.hole_polygon, self.transform.position.x, self.transform.position.y, self.lifetime if self.screen_chunk_collision_enabled else -1, self.screen_chunk_collision_enabled)
    # Create the hole object
    self.hole = Hole(self, self.hole_polygon, self.transform.position.x, self.transform.position.y, self.lifetime)
    self.hole.tk_obj.lower(self.screen_chunk.tk_obj)

  def update(self):
    super().update()
    if self.screen_chunk and self.screen_chunk.transform.position.y > Environment.height:
      self.screen_chunk.destroy()
      self.screen_chunk = None

    if self.screen_chunk and self.screen_chunk.tk_obj == None:
      self.screen_chunk = None

    if self.hole and self.hole.tk_obj == None:
      self.hole = None

    if self.screen_chunk == None and self.hole == None:
      self.destroy()
      return