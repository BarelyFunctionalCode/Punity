import platform

from engine import Environment
from engine.object import Object

from .border import Border
from .editor import Editor


class Scene(Object):
  def __init__(self, create_editor=False):
    super().__init__()
    self.editor = None
    Environment.set_root(self)

    if platform.system() == 'Darwin':
      # Set application activation policy to not allow menubar, dock, or application focus
      import AppKit
      AppKit.NSApp.setActivationPolicy_(AppKit.NSApplicationActivationPolicyProhibited)

    Border(self, Environment.width, Environment.height, Environment.x, Environment.y, 50)

    # Create the editor
    if create_editor:
      self.editor = Editor(self, True)

  # Begins the main loop for the root object
  def begin(self):
    try:
      self.tk_obj.mainloop()
    except:
      self.destroy()