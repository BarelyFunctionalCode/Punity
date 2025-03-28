from engine import Environment, Object
from engine.graphics import Text
from .container import ToastContainer

class Toast(Object):
  def __init__(self, text, lifetime=-1):
    self.text = text
    self.lifetime = lifetime
    self.lifetime_timer = 0
    self.text_obj = None

    # Check for existing toast container
    for obj in Environment.objects:
      if isinstance(obj, ToastContainer):
        parent = obj
        break
    
    # If no container found, create one
    else:
      parent = ToastContainer(Environment.root, 0, 0)

    super().__init__(parent, "toast", 300, max(int(25 * (len(self.text) / 35)), 50), Environment.x - 300, Environment.y + 5, False)
    self.collision_enabled = False

  def start(self):
    super().start()
    self.lifetime_timer = 0
    self.tk_obj['bg'] = "#333"

    self.text_obj = Text(self, self.text, 5, 5, anchor="nw", font=("Courier New", 15), fill="white", width=290)



  def update(self):
    super().update()
    if self.lifetime == -1:
      return
    self.lifetime_timer += self.delta_time
    if self.lifetime_timer > self.lifetime:
      self.fade_out()
      if self.is_faded:
        self.destroy()