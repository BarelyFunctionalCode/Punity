from .control_menu import ControlMenu
from .inspector import Inspector
from .hierarchy import Hierarchy


class Editor:
  def __init__(self, parent, force_expand=False):
    self.controls_menu = ControlMenu(parent)
    self.inspector = Inspector(parent)
    self.hierarchy = Hierarchy(parent, self.inspector, force_expand)