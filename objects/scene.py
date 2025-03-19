from .object import Object
from .border import Border
from .editor import Editor

from environment import Instance as environment

class Scene(Object):
  def __init__(self, create_editor=False):
    super().__init__()
    environment.set_root(self)

    # Create the border objects for the screen
    Border(self, environment.width, environment.height, environment.x, environment.y, 50)

    # Create the editor
    if create_editor:
      Editor(self, True)

  # Begins the main loop for the root object
  def begin(self):
    try:
      self.tk_obj.mainloop()
    except:
      self.destroy()