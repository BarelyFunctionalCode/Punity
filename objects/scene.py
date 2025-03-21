import platform

from .object import Object
from .border import Border
from .editor import Editor

from environment import environment

class Scene(Object):

  def __init__(self, create_editor=False):
    super().__init__()
    self.editor = None
    environment.set_root(self)

    if platform.system() == 'Darwin':
      # Set application activation policy to not allow menubar, dock, or application focus
      import AppKit
      AppKit.NSApp.setActivationPolicy_(AppKit.NSApplicationActivationPolicyProhibited)

    Border(self, environment.width, environment.height, environment.x, environment.y, 50)

    # Create the editor
    if create_editor:
      self.editor = Editor(self, True)

  # Begins the main loop for the root object
  def begin(self):
    try:
      self.tk_obj.mainloop()
    except:
      self.destroy()