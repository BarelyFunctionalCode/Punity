from Punity.engine import Object
from Punity.engine.math import Side


class BorderSide(Object):
  def __init__(self, parent, side: Side, width, height, x, y, thickness):
    if side == Side.TOP:
      params = [width, thickness, x, y - thickness - 25]
    elif side == Side.RIGHT:
      params = [thickness, height, x + width, y]
    elif side == Side.BOTTOM:
      params = [width, thickness, x, y + height]
    elif side == Side.LEFT:
      params = [thickness, height, x - thickness, y]

    name = f"{side.name}_bound"
    super().__init__(parent, name, *params, True)

  def start(self):
    super().start()
    self.collision_enabled = True

  # def paint(self, p):
  #   p.setFillStyle(QColorConstants.Red)
  #   p.fillRect(self.transform.position.x - self.transform.width*5, self.transform.position.y - self.transform.height*5, self.transform.width*10, self.transform.height*10)


# Created objects to represent the border of the screen, which allows for collision detection
class Border:
  def __init__(self, parent, width, height, x, y, thickness):
    self.top = BorderSide(parent, Side.TOP, width, height, x, y, thickness)
    self.right = BorderSide(parent, Side.RIGHT, width, height, x, y, thickness)
    self.bottom = BorderSide(parent, Side.BOTTOM, width, height, x, y, thickness)
    self.left = BorderSide(parent, Side.LEFT, width, height, x, y, thickness)