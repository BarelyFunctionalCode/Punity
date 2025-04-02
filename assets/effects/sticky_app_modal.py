from engine import Object

from assets.components.leech import Leech
from assets.objects.modal import Modal


class StickyAppModal(Object, Leech):
  def __init__(self, parent, window_name, modal_width, modal_height, title='', text_content='', buttons=[], button_actions={}):
    self.modal_width = modal_width
    self.modal_height = modal_height
    self.title = title
    self.text_content = text_content
    for button in buttons:
      if 'action' not in button:
        button['action'] = 'close'
    self.buttons = buttons
    self.button_actions = {**button_actions, 'close': lambda _: self.destroy()}
    self.modal = None
    super().__init__(parent, 'StickyAppModal', 0, 0, 0, 0, False, window_name=window_name, auto_size=True)
  
  def update(self):
    super().update()
    if self.is_leech_attached and not self.modal:

      self.modal = Modal(
        self,
        self.modal_width,
        self.modal_height,
        title=self.title,
        text_content=self.text_content,
        buttons=self.buttons,
        button_actions=self.button_actions
      )

    if not self.is_leech_attached and self.modal:
      self.modal.destroy()
      self.modal = None