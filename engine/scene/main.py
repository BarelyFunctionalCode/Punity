import platform

from engine import Environment, Object

from .border import Border
from .editor import Editor


class Scene(Object):
  def __init__(self, dev_mode=False):
    super().__init__()
    self.editor = None
    Environment.set_root(self)

    if platform.system() == 'Darwin':
      # Set application activation policy to not allow menubar, dock, or application focus
      import AppKit
      AppKit.NSApp.setActivationPolicy_(AppKit.NSApplicationActivationPolicyProhibited)
      
    Environment.start_input_event_monitor()

    Border(self, Environment.width, Environment.height, Environment.x, Environment.y, 50)

    # Create the editor
    if dev_mode:
      Environment.dev_mode = True
      self.editor = Editor(self, True)
    
    self._update()

  def _update(self):
    for obj in self.children:
      obj._update()

    self.tk_obj.after(10, self._update)

  # Begins the main loop for the root object
  def begin(self):
    try:
      self.tk_obj.mainloop()
    except:
      self.destroy()