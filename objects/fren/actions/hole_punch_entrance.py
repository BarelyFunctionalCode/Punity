from effects.hole_punch import HolePunch
from objects.screen_chunk import ScreenChunk
from objects.object import Object
from utils import invis_tk, Vector2
import tkinter as tk

class HolePunchEntrance(Object):
  spawn_position = Vector2([500, 200])

  def __init__(self, parent, fren):
    self.polygon = fren.face_polygon
    if self.polygon == None:
      self.polygon = [0,0, 200,0, 200,200, 0,200]

    # Offset from the hole punch and the extra screen chunk
    min_x = min(self.polygon[::2])
    max_x = max(self.polygon[::2])
    offset = max_x - min_x - 100

    # Initialize base Tkinter window
    root = invis_tk(tk.Toplevel(parent))
    name = f"hole_punch_entrance_{id(self)}"
    root.title(name)
    root.geometry(f"0x0+{HolePunchEntrance.spawn_position.x - offset}+{HolePunchEntrance.spawn_position.y}")

    # Hole Punch
    self.hole_punch = HolePunch(root, self.polygon, HolePunchEntrance.spawn_position.x - offset, HolePunchEntrance.spawn_position.y, 5000)
    self.hole_punch.screen_chunk.collision_ignore_list.append(fren.name)
    super().__init__(name, root, True)

  def post_fren_spawn(self):
    self.hole_punch.screen_chunk.root.lift()

  def trigger(self, fren):
    # Screen Chunk for Fren to hide behind
    self.screen_chunk = ScreenChunk(self.root, self.polygon, self.transform.position.x, self.transform.position.y, 5000, True, True, Vector2([250, 200]), Vector2([-85, 0]))

    # After a second, push Fren out from behind the screen chunk
    self.root.after(1000, lambda: fren.apply_force(Vector2.left * 10))
    self.root.after(1500, lambda: fren.set_face_expression("slow_scan"))

  def update(self):
    super().update() if hasattr(super(), 'update') else None

    if self.hole_punch and self.hole_punch.root == None:
      self.hole_punch = None

    if hasattr(self, 'screen_chunk') and self.screen_chunk and self.screen_chunk.root == None:
      self.screen_chunk = None

    if self.hole_punch == None and self.screen_chunk == None:
      self.destroy()
      return
    