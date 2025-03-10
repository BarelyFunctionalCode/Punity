import tkinter as tk

from objects.object import Object
from utils import invis_tk

class Hole(Object):
  def __init__(self, parent, hole_polygon, x, y, lifetime=-1):
    # Get min/max x/y values
    min_x = min(hole_polygon[::2])
    max_x = max(hole_polygon[::2])
    min_y = min(hole_polygon[1::2])
    max_y = max(hole_polygon[1::2])

    # Get width and height
    width = max_x - min_x
    height = max_y - min_y

    # Initialize base Tkinter window
    root = invis_tk(tk.Toplevel(parent))
    root.geometry(f"{width}x{height}+{x}+{y}")

    root.update_idletasks()

    # Make empty canvas
    self.graphic_canvas = tk.Canvas(root, width=width, height=height, bg=root['bg'], bd=0, highlightthickness=0, cursor='none')
    self.graphic_canvas.pack(padx=0, pady=0, side=tk.TOP)

    # Draw hole polygon
    self.graphic_canvas.create_polygon(hole_polygon, fill='black', outline=root['bg'])

    name = f"hole_{id(self)}"

    self.lifetime = lifetime
    self.lifetime_timer = 0
    super().__init__(name, root, True)

  def start(self):
    super().start() if hasattr(super(), 'start') else None

  def update(self):
    super().update() if hasattr(super(), 'update') else None

    if self.lifetime == -1:
      return
    self.lifetime_timer += self.delta_time
    if self.lifetime_timer > self.lifetime:
      if self.root.wm_attributes("-alpha") > 0.0:
        self.root.wm_attributes("-alpha", self.root.wm_attributes("-alpha") - 0.05)
        self.root.after(50, self.update)
        return
      self.destroy()
      return