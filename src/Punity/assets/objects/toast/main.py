import math

from Punity.engine import Environment, Object
from Punity.engine.graphics import Text, Rectangle
from .container import ToastContainer


class Toast(Object):
  def __init__(self, text, lifetime=-1, bg_color="white", text_color="black", line_height=15):
    self.text = text
    self.lifetime = lifetime
    self.lifetime_timer = 0
    self.text_obj = None
    self.bg_color = bg_color
    self.text_color = text_color
    self.line_height = line_height
    self.padding = 20

    # Check for existing toast container
    for obj in Environment.objects:
      if isinstance(obj, ToastContainer):
        parent = obj
        break
    
    # If no container found, create one
    else:
      parent = ToastContainer()

    super().__init__(parent, "toast", 300, (self.line_height + self.padding) * math.ceil(len(self.text) / 35), -500, 0, False)

    self.collision_enabled = False

  def start(self):
    super().start()
    self.lifetime_timer = 0

    self.background = Rectangle(self, [0, 0, self.transform.width, self.transform.height], fill=self.bg_color, rounded_corners=20)
    self.text_obj = Text(self, self.text, font_size=self.line_height, fill=self.text_color)
    self.update_visuals()

  def update(self):
    super().update()
    if self.lifetime == -1:
      return
    self.lifetime_timer += self.delta_time
    if self.lifetime_timer > self.lifetime:
      self.fade_out()
      if self.is_faded:
        self.destroy()