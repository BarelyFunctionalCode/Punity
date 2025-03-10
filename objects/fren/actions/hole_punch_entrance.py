from effects.hole_punch import HolePunch
from objects.screen_chunk import ScreenChunk
from objects.object import Object
from utils import Vector2

class HolePunchEntrance(Object):
  spawn_position = Vector2([500, 200])

  def __init__(self, parent, fren):
    self.fren = fren
    self.polygon = fren.face_polygon
    if self.polygon == None:
      self.polygon = [0,0, 200,0, 200,200, 0,200]
    # Offset from the hole punch and the extra screen chunk
    min_x = min(self.polygon[::2])
    max_x = max(self.polygon[::2])
    self.offset = max_x - min_x - 100
    super().__init__(parent, 'hole_punch_entrance', 0, 0, HolePunchEntrance.spawn_position.x - self.offset, HolePunchEntrance.spawn_position.y, True)


  def start(self):
    super().start() if hasattr(super(), 'start') else None
    # Hole Punch
    self.hole_punch = HolePunch(self.root, self.polygon, HolePunchEntrance.spawn_position.x - self.offset, HolePunchEntrance.spawn_position.y, 5000)
    self.hole_punch.screen_chunk.collision_ignore_list.append(self.fren.name)
    self.fren.root.lift(self.hole_punch.hole.root)

    # Screen Chunk for Fren to hide behind
    self.screen_chunk = ScreenChunk(self.root, self.polygon, self.transform.position.x, self.transform.position.y, 5000, True, True, Vector2([250, 200]), Vector2([-85, 0]))

    # After a second, push Fren out from behind the screen chunk
    self.root.after(1000, lambda: self.fren.apply_force(Vector2.left * 10))
    self.root.after(1500, lambda: self.fren.set_face_expression("slow_scan"))


  def update(self):
    super().update() if hasattr(super(), 'update') else None

    if self.hole_punch and self.hole_punch.root == None:
      self.hole_punch = None

    if self.screen_chunk and self.screen_chunk.root == None:
      self.screen_chunk = None

    if self.hole_punch == None and self.screen_chunk == None:
      self.destroy()
      return
    