import tkinter as tk
import pyautogui
from PIL import ImageTk, Image, ImageDraw

from objects.object import Object
from utils import invis_tk

class ScreenChunk(Object):
  def __init__(self, parent, polygon, x, y, lifetime=-1, is_static=True):
    # Get min/max x/y values
    min_x = min(polygon[::2])
    max_x = max(polygon[::2])
    min_y = min(polygon[1::2])
    max_y = max(polygon[1::2])

    # Get width and height
    width = max_x - min_x
    height = max_y - min_y

    # Take screenshot of the screen chunk
    screenshot = pyautogui.screenshot(region=(x, y, width, height))

    # Initialize base Tkinter window
    root = invis_tk(tk.Toplevel(parent))
    root.geometry(f"{width}x{height}+{x}+{y}")

    root.update_idletasks()

    # Make empty canvas
    self.graphic_canvas = tk.Canvas(root, bg=root['bg'], bd=0, highlightthickness=0, cursor='none')
    self.graphic_canvas.pack(fill=tk.BOTH, padx=0, pady=0, side=tk.TOP)

    # Apply the mask to the screenshot
    self.graphic_canvas.create_polygon(polygon, fill='black', outline=root['bg'])
    self.chunk_image = ImageTk.PhotoImage(screenshot)
    self.graphic_canvas.create_image(0, 0, image=self.chunk_image, anchor=tk.NW)
    

    name = f"screen_chunk_{id(self)}"

    self.lifetime = lifetime
    self.lifetime_timer = 0
    super().__init__(name, root, is_static)

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