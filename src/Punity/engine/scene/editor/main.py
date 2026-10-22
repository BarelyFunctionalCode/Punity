from .control_menu import ControlMenu
from .inspector import Inspector
from .hierarchy import Hierarchy


class Editor:
  def __init__(self, parent, force_expand=False):
    self.parent = parent
    self.force_expand = force_expand
    self.controls_menu = ControlMenu(self, parent)
    self.inspector = None
    self.hierarchy = None
  
  def create_inspector(self):
    self.inspector = Inspector(self.parent)
    if self.hierarchy.inspector is None:
      self.hierarchy.inspector = self.inspector
  
  def destroy_inspector(self):
    self.inspector.inspector.destroy()
    self.inspector = None

  def create_hierarchy(self):
    self.hierarchy = Hierarchy(self.parent, self.inspector, self.force_expand)

  def destroy_hierarchy(self):
    self.hierarchy.hierarchy.destroy()
    self.hierarchy = None