from effects.hole_punch import HolePunch
from objects.screen_chunk import ScreenChunk
from objects.object import Object
from utils import invis_tk, Vector2
import tkinter as tk

from ..main import Fren

class HolePunchEntrance(Object):
  def __init__(self, parent, x, y):
    # Initialize base Tkinter window
    root = invis_tk(tk.Toplevel(parent))
    name = f"hole_punch_entrance_{id(self)}"

    # Hole Punch
    self.hole_punch = HolePunch(root, [0,0, 200,0, 200,300, 0,300], x, y, 5000)

    # Fren
    self.fren = Fren('fren', parent, x + 200, y)

    # Screen Chunk for Fren to hide behind
    self.screen_chunk = ScreenChunk(root, [0,0, 200,0, 200,300, 0,300], x + 200, y, 5000, True)

    super().__init__(name, root, True)

  def start(self):
    super().start() if hasattr(super(), 'start') else None

    self.root.after(1000, self.apply_force)

  def apply_force(self):
    self.fren.apply_force(Vector2.left * 10)


  def update(self):
    super().update() if hasattr(super(), 'update') else None

    if self.hole_punch and self.hole_punch.root == None:
      self.hole_punch = None

    if self.screen_chunk and self.screen_chunk.root == None:
      self.screen_chunk = None

    if self.hole_punch == None and self.screen_chunk == None:
      self.destroy()
      return
    