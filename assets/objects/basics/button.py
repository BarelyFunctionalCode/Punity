from PySide6.QtCore import QRect

from engine import Object
from engine.graphics import Text, Rectangle


class Button(Object):
  def __init__(self, parent, width, height, x, y, text='', action=None, background="white", color="black"):
    self.text = text
    self.button_obj = {}
    self.action = action
    self.background = background
    self.color = color
    super().__init__(parent, 'Button', width, height, x, y)

    self.inactive_time = 1000
    self.inactive_timer = 0

  def start(self):
    super().start()

    # Create the buttons
    self.button_obj['rect'] = Rectangle(
      self,
      [0, 0, self.transform.width, self.transform.height],
      fill=self.background,
      rounded_corners=5
    )
    self.button_obj['text'] = Text(
      self,
      self.text,
      x=self.transform.width // 2,
      y=self.transform.height // 2,
      font_size=min(self.transform.width, self.transform.height) // 2 - 10,
      fill=self.color,
    )

  def update(self):
    super().update()

    if self.inactive_timer < self.inactive_time:
      self.inactive_timer += self.delta_time
    
    self.button_obj['text'].opacity = min(self.inactive_timer / self.inactive_time, 1.0)

  def post_update(self, did_geomentry_update):
    super().post_update(did_geomentry_update)

    if did_geomentry_update:
      self.button_obj['rect'].shape_data = [0, 0, self.transform.width, self.transform.height]
      self.button_obj['text'].x = self.transform.width // 2
      self.button_obj['text'].y = self.transform.height // 2
      self.button_obj['text'].font_size = min(self.transform.width, self.transform.height) // 2 - 10
      self.inactive_timer = 0

  def destroy(self):
    self.set_inputs(False)
    super().destroy()

  def mouse_event(self, event):
    if self.inactive_timer < self.inactive_time:
      return
    
    window_position = self.transform.position

    button_rect = QRect(
      window_position.x,
      window_position.y,
      self.transform.width,
      self.transform.height
    )
    if button_rect.contains(event.position().toPoint()):
      if self.action != None:
        self.action(event)