from .object import Object
from utils import Side, TkMimic

class BorderSide(Object):
  def __init__(self, side: Side, x, y, width, height, thickness):
    if side == Side.TOP:
      root = TkMimic(x, y - thickness, width, thickness)
    elif side == Side.RIGHT:
      root = TkMimic(x + width, y, thickness, height)
    elif side == Side.BOTTOM:
      root = TkMimic(x, y + height, width, thickness)
    elif side == Side.LEFT:
      root = TkMimic(x - thickness, y, thickness, height)

    name = f"{side.name}_bound"
    super().__init__(name, root, True)

  def start(self):
    super().start() if hasattr(super(), 'start') else None
    self.collision_enabled = True

class Border:
  def __init__(self, x, y, width, height, thickness):
    self.top = BorderSide(Side.TOP, x, y, width, height, thickness)
    self.right = BorderSide(Side.RIGHT, x, y, width, height, thickness)
    self.bottom = BorderSide(Side.BOTTOM, x, y, width, height, thickness)
    self.left = BorderSide(Side.LEFT, x, y, width, height, thickness)