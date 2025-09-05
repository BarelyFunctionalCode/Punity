from engine import Object
from engine.math import Vector2

from assets.effects.hole_punch import HolePunch
from assets.objects.screen_chunk import ScreenChunk



class HolePunchEntrance(Object):
  spawn_position = Vector2([500, 200])

  def __init__(self, parent, fren):
    self.fren = fren
    self.polygon = list(fren.face_polygon)
    if self.polygon == None:
      self.polygon = [-10,-10, 200,-10, 200,200, -10,200]
    # Offset from the hole punch and the extra screen chunk
    min_x = min(self.polygon[::2])
    max_x = max(self.polygon[::2])
    self.offset = max_x - min_x - 100
    self.runtime = 0

    self.sequence = [
      {'time': 1000, 'action': lambda: self.fren.apply_force(Vector2.left * 10)},
      {'time': 1300, 'action': lambda: self.fren.tk_obj.lift(self.screen_chunk.tk_obj)},
      {'time': 1500, 'action': lambda: self.fren.set_face_expression("slow_scan")}
    ]
    self.sequence_index = 0

    super().__init__(parent, 'hole_punch_entrance', 0, 0, HolePunchEntrance.spawn_position.x - self.offset, HolePunchEntrance.spawn_position.y, True)

  def start(self):
    super().start()
    # Hole Punch
    self.hole_punch = HolePunch(self, self.polygon, HolePunchEntrance.spawn_position.x - self.offset, HolePunchEntrance.spawn_position.y, 5000)
    self.hole_punch.screen_chunk.collision_ignore_list.append(self.fren.name)
    self.fren.tk_obj.lift(self.hole_punch.hole.tk_obj)

    # Screen Chunk for Fren to hide behind
    self.screen_chunk = ScreenChunk(self, self.polygon, self.transform.position.x, self.transform.position.y, 5000, True, Vector2([250, 200]), Vector2([-85, 0]))
    self.hole_punch.screen_chunk.tk_obj.lift(self.screen_chunk.tk_obj)

  def update(self):
    super().update()

    # Run the sequence
    self.runtime += self.delta_time
    if self.sequence_index < len(self.sequence):
      if self.runtime > self.sequence[self.sequence_index]['time']:
        self.sequence[self.sequence_index]['action']()
        self.sequence_index += 1

    if self.hole_punch and self.hole_punch.tk_obj == None:
      self.hole_punch = None

    if self.screen_chunk and self.screen_chunk.tk_obj == None:
      self.screen_chunk = None

    if self.hole_punch == None and self.screen_chunk == None:
      self.destroy()
      return
    