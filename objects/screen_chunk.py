import tkinter as tk
import pyautogui
from PIL import ImageTk, Image, ImageDraw

from objects.object import Object

class ScreenChunk(Object):
  def __init__(self, parent, polygon, x, y, lifetime=-1, is_static=True, invert=False, invert_size=None, invert_point=None):
    self.polygon = polygon
    self.lifetime = lifetime
    self.invert = invert
    self.invert_size = invert_size
    self.invert_point = invert_point

    # Get min/max x/y values
    min_x = min(polygon[::2])
    max_x = max(polygon[::2])
    min_y = min(polygon[1::2])
    max_y = max(polygon[1::2])
    # Get width and height
    width = invert_size.x if invert else max_x - min_x
    height = invert_size.y if invert else max_y - min_y
    # Update x and y values if inverted
    x -= invert_point.x if invert else 0
    y -= invert_point.y if invert else 0
    super().__init__(parent, 'screen_chunk', width, height, x, y, is_static)
    

  def start(self):
    super().start() if hasattr(super(), 'start') else None
    x = int(self.transform.position.x)
    y = int(self.transform.position.y)
    width = self.transform.width
    height = self.transform.height

    # Invert the polygon if needed
    if self.invert:
      self.collision_enabled = False
      for i in range(len(self.polygon)):
        if i % 2 == 0:
          self.polygon[i] = self.invert_point.x + self.polygon[i]
        else:
          self.polygon[i] = self.invert_point.y + self.polygon[i]
      for i in range(0, len(self.polygon), 2):
        if self.polygon[i] < 0:
          self.polygon[i] = 0
        if self.polygon[i] > width:
          self.polygon[i] = width
      for i in range(1, len(self.polygon), 2):
        if self.polygon[i] < 0:
          self.polygon[i] = 0
        if self.polygon[i] > height:
          self.polygon[i] = height
      self.polygon = [*[0,0, 0,height, width,height, width,0, 0,0], *self.polygon, *[0,0]]

    # Take screenshot of the screen chunk
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    # Make empty canvas
    self.graphic_canvas = tk.Canvas(self.tk_obj, bg=self.tk_obj['bg'], width=width, height=height, bd=0, highlightthickness=0, cursor='none')
    # self.graphic_canvas = tk.Canvas(tk_obj, bg=tk_obj['bg'], width=width, height=height, bd=3, highlightthickness=3, cursor='none', highlightbackground='red')
    self.graphic_canvas.pack(padx=0, pady=0, side=tk.TOP)

    # Apply the mask to the screenshot (Required for MacOS)
    self.graphic_canvas.create_polygon(self.polygon, fill='black', outline=self.tk_obj['bg'], width=0)

    # Mask screenshot to polygon (Works on Windows)
    screenshot = screenshot.crop((0, 0, width, height))
    mask = Image.new('L', (width, height), 0)
    ImageDraw.Draw(mask).polygon(self.polygon, outline=0, fill=255)
    screenshot.putalpha(mask)
    
    # convert to ImageTk format
    self.chunk_image = ImageTk.PhotoImage(screenshot)
    self.graphic_canvas.create_image(0, 0, image=self.chunk_image, anchor=tk.NW)

    self.lifetime_timer = 0


  def update(self):
    super().update() if hasattr(super(), 'update') else None
    if self.lifetime == -1:
      return
    self.lifetime_timer += self.delta_time
    if self.lifetime_timer > self.lifetime:
      if self.tk_obj.wm_attributes("-alpha") > 0.0:
        self.tk_obj.wm_attributes("-alpha", self.tk_obj.wm_attributes("-alpha") - 0.05)
        self.tk_obj.after(50, self.update)
        return
      self.destroy()
      return