import tkinter as tk

from engine.object import Object


class Hole(Object):
  def __init__(self, parent, hole_polygon, x, y, lifetime=-1):
    self.hole_polygon = hole_polygon
    self.lifetime = lifetime

    # Get min/max x/y values
    min_x = min(hole_polygon[::2])
    max_x = max(hole_polygon[::2])
    min_y = min(hole_polygon[1::2])
    max_y = max(hole_polygon[1::2])
    # Get width and height
    width = max_x - min_x
    height = max_y - min_y
    super().__init__(parent, "hole", width, height, x, y, True)

  def start(self):
    super().start()
    # Make empty canvas
    self.graphic_canvas = tk.Canvas(self.tk_obj, width=self.transform.width, height=self.transform.height, bg=self.tk_obj['bg'], bd=0, highlightthickness=0, cursor='none')
    self.graphic_canvas.pack(padx=0, pady=0, side=tk.TOP)
    # Draw hole polygon
    self.graphic_canvas.create_polygon(self.hole_polygon, fill='black', outline=self.tk_obj['bg'])
    self.lifetime_timer = 0

  def update(self):
    super().update()
    if self.lifetime == -1:
      return
    self.lifetime_timer += self.delta_time
    if self.lifetime_timer > self.lifetime:
      self.fade_out()
      if self.is_faded:
        self.destroy()