import tkinter as tk

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
    self.button_actions = button_actions
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
    self.tk_obj.wm_attributes("-alpha", 0.5)
    self.tk_obj.config(bg='black')

    
    # Create the modal window
    self.popup = ModalPopup(self, self.modal_width, self.modal_height, self.modal_x, self.modal_y, title=self.title, text_content=self.text_content, buttons=self.buttons, button_actions=self.button_actions)
    self.popup.tk_obj.transient(self.tk_obj)  # Make the modal window transient to the main window


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
    self.tk_obj.config(bg='#333')
    self.tk_obj.config(cursor='hand2')

    # Create the title
    self.title_obj = {}
    self.title_obj['rect'] = Rectangle(self, [0, 0, self.transform.width, 20], fill='#555', width=0)
    self.title_obj['text'] = Text(self, self.title, 5, 5, anchor="nw", font=("Courier New", 12), fill="white")
    # Create the text content
    self.text_obj = Text(
      self,
      self.text_content,
      self.transform.width // 2,
      self.transform.height // 2 - 50,
      font=("Courier New", 15), fill="white"
    )
    # Create the buttons
    self.button_objs = []
    for i, button in enumerate(self.buttons):
      button_obj = {}
      x_pos = self.transform.width // 2 - ((len(self.buttons) - 1) * (self.button_size.x + 10)) // 2 + i * (self.button_size.x + 10)
      y_pos = self.transform.height - self.button_size.y // 2 - 10
      button_obj['rect'] = Rectangle(
        self,
        [x_pos - self.button_size.x // 2, y_pos - self.button_size.y // 2, x_pos + self.button_size.x // 2, y_pos + self.button_size.y // 2],
        fill='#555',
      )
      button_obj['text'] = Text(
        self,
        button['text'],
        x_pos,
        y_pos,
        width=self.button_size.x,
        font=("Courier New", 15),
        fill="white",
        tags=[button_obj['rect'].name]
      )
      button_obj['rect'].bind("<Button-1>", lambda event: self.button_actions[button['action']](event))
      self.button_objs.append(button_obj)