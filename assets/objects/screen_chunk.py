from PIL import Image, ImageDraw
import tkinter as tk
import pyautogui
import shapely

from engine import Object
from engine.graphics import Sprite


class ScreenChunk(Object):
  def __init__(self, parent, polygon, x, y, lifetime=-1, is_static=True, invert_size=None, invert_point=None):
    self.polygon = polygon
    self.lifetime = lifetime
    self.invert_size = invert_size
    self.invert_point = invert_point
    self.invert = False if invert_size is None else True

    # Get min/max x/y values
    min_x = min(polygon[::2])
    max_x = max(polygon[::2])
    min_y = min(polygon[1::2])
    max_y = max(polygon[1::2])
    # Get width and height
    width = invert_size.x if self.invert else max_x - min_x
    height = invert_size.y if self.invert else max_y - min_y
    # Update x and y values if inverted
    x -= invert_point.x if self.invert else 0
    y -= invert_point.y if self.invert else 0
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
      # Remove any polygon points that are outside the bounds
      for i in range(len(self.polygon)):
        if i % 2 == 0:
          self.polygon[i] = int(self.invert_point.x) + self.polygon[i]
        else:
          self.polygon[i] = int(self.invert_point.y) + self.polygon[i]

      # Remove the polygon shape from the bounds
      bounds = shapely.geometry.box(0, 0, width, height)
      poly = shapely.geometry.Polygon([(self.polygon[i], self.polygon[i+1]) for i in range(0, len(self.polygon), 2)])
      diff = bounds.difference(poly)
      self.polygon = list(diff.exterior.coords)

    # Take screenshot of the screen chunk
    screenshot = pyautogui.screenshot(region=(x, y, width, height))

    # Mask screenshot to polygon
    screenshot = screenshot.crop((0, 0, width, height))
    mask = Image.new('L', (width, height), 0)
    ImageDraw.Draw(mask).polygon(self.polygon, outline=255, fill=255)
    screenshot.putalpha(mask)
    
    # Create sprite
    Sprite(self, screenshot, 0, 0, anchor=tk.NW)

    self.lifetime_timer = 0

  def update(self):
    super().update() if hasattr(super(), 'update') else None
    if self.lifetime == -1:
      return
    self.lifetime_timer += self.delta_time
    if self.lifetime_timer > self.lifetime:
      self.fade_out()
      if self.is_faded:
        self.destroy()