from PySide6.QtCore import QRect
from PySide6.QtCanvasPainter import QCanvasPainter

from engine import Environment, Object
from engine.math import Vector2
from engine.graphics import Text, Rectangle


class Modal(Object):
  def __init__(self, parent, modal_width, modal_height, title='', text_content='', buttons=[], button_actions={}, is_static=False, **kwargs):
    self.modal_width = modal_width
    self.modal_height = modal_height
    self.title = title
    self.text_content = text_content
    self.buttons = buttons
    self.button_actions = {**button_actions, 'close': lambda _: self.destroy()}
    if len(buttons) == 0:
      self.buttons = [{'text': 'OK', 'action': 'close'}]

    width = parent.transform.width if parent.transform.width > 1 else Environment.width
    height = parent.transform.height if parent.transform.height > 1 else Environment.height
    x = int(parent.transform.position.x)
    y = int(parent.transform.position.y)

    self.modal_x = x + (width - modal_width) // 2
    self.modal_y = y + (height - modal_height) // 2
    self.popup = None
    super().__init__(parent, 'Modal', width, height, x, y, is_static, **kwargs)

  def start(self):
    super().start()

    # Create the overlay
    Rectangle(self, [0, 0, self.transform.width, self.transform.height], fill="#1A1A1A", opacity=0.5)
    
    # Create the modal window
    self.popup = ModalPopup(self, self.modal_width, self.modal_height, self.modal_x, self.modal_y, title=self.title, text_content=self.text_content, buttons=self.buttons, button_actions=self.button_actions)

  def destroy(self):
    if self.popup:
      self.popup.destroy()
    super().destroy()

class ModalPopup(Object):
  def __init__(self, parent, width, height, x, y, title='', text_content='', buttons=[], button_actions={}):
    self.title = title
    self.text_content = text_content
    self.button_size = Vector2([100, 20])
    self.buttons = buttons
    self.button_actions = button_actions
    super().__init__(parent, 'ModalPopup', width, height, x, y, parent.is_static)

  def start(self):
    super().start()
    Rectangle(self, [0, 0, self.transform.width, self.transform.height], fill='#333')

    # Create the title
    self.title_obj = {}
    self.title_obj['rect'] = Rectangle(self, [0, 0, self.transform.width, 20], fill='#555')
    self.title_obj['text'] = Text(self, self.title, x=3, y=3, text_align=QCanvasPainter.TextAlign.Left, text_baseline=QCanvasPainter.TextBaseline.Hanging, font_size=14, fill="white")
    # Create the text content
    self.text_obj = Text(self, self.text_content, fill="white")
    # Create the buttons
    self.button_objs = []
    for i, button in enumerate(self.buttons):
      button_obj = {}
      x_pos = self.transform.width // 2 - ((len(self.buttons) - 1) * (self.button_size.x + 10)) // 2 + i * (self.button_size.x + 10)
      y_pos = self.transform.height - self.button_size.y // 2 - 10
      button_obj['rect'] = Rectangle(
        self,
        [x_pos - self.button_size.x // 2, y_pos - self.button_size.y // 2, self.button_size.x, self.button_size.y],
        fill='#555',
        rounded_corners=5
      )
      button_obj['text'] = Text(
        self,
        button['text'],
        x=x_pos,
        y=y_pos,
        font_size=14,
        fill="white",
      )
      self.button_objs.append(button_obj)
    self.set_inputs(True)

  def destroy(self):
    self.set_inputs(False)
    super().destroy()

  def mouse_event(self, event):
    window_position = self.transform.position
    for i, button in enumerate(self.buttons):
      x_pos = self.transform.width // 2 - ((len(self.buttons) - 1) * (self.button_size.x + 10)) // 2 + i * (self.button_size.x + 10)
      y_pos = self.transform.height - self.button_size.y // 2 - 10

      button_rect = QRect(
        window_position.x + x_pos - self.button_size.x // 2,
        window_position.y + y_pos - self.button_size.y // 2,
        self.button_size.x,
        self.button_size.y
      )
      if button_rect.contains(event.position().toPoint()):
        if button['action'] in self.button_actions:
          self.button_actions[button['action']](event)