import numpy as np
from PySide6.QtGui import QColor
from PySide6.QtCore import QRectF

from Punity.engine.graphics.main import Graphic


class _Shape(Graphic):
  def __init__(self, parent, name, shape_data, min_shape_data=0, required_shape_data=0, shape_contraint_text="", **kwargs):
    if type(shape_data) not in [list, tuple] or len(shape_data) < min_shape_data or len(shape_data) < required_shape_data:
      shape_contraint_text = f"at least {min_shape_data}" if min_shape_data > 0 else f"exactly {required_shape_data}"
      raise ValueError(f"shape_data must be a list{ ' with ' + shape_contraint_text + ' elements' if shape_contraint_text else ''}\n\nshape_data: {shape_data}")

    self._fill = None
    self._hole_rect = None
    self._stroke = None
    self._opacity = 1.0
    self._shape_data = None
    
    super().__init__(parent, name)

    self.shape_data = shape_data
    self.fill = kwargs.get("fill", None)
    self.stroke = kwargs.get("stroke", None)
    self.opacity = kwargs.get("opacity", 1.0)


  @property
  def fill(self):
    return self._fill

  @property
  def hole_rect(self):
    return self._hole_rect

  @property
  def stroke(self):
    return self._stroke

  @property
  def opacity(self):
    return self._opacity

  @property
  def shape_data(self):
    return self._shape_data
  
  @fill.setter
  def fill(self, value):
    if value is not None:
      old_fill = self._fill
      self._fill = QColor(value)
      self._fill.setAlphaF(self.opacity)
      if old_fill != self._fill:
        self.parent.update_visuals()

  @stroke.setter
  def stroke(self, value):
    if value is not None:
      old_stroke = self._stroke
      self._stroke = QColor(value)
      self._stroke.setAlphaF(self.opacity)
      if old_stroke != self._stroke:
        self.parent.update_visuals()

  @hole_rect.setter
  def hole_rect(self, value):
    if value[2] <= 0 or value[3] <= 0:
      value = None
    if value != self._hole_rect:
      self._hole_rect = value
      self.parent.update_visuals()

  @opacity.setter
  def opacity(self, value):
    if value == self._opacity:
      return
    self._opacity = min(max(value, 0.0), 1.0)
    if self._fill is not None:
      self._fill.setAlphaF(self._opacity)
    if self._stroke is not None:
      self._stroke.setAlphaF(self._opacity)
    self.parent.update_visuals()

  @shape_data.setter
  def shape_data(self, value):
    old_shape_data = self._shape_data
    self._shape_data = value
    if old_shape_data != self._shape_data:
      self.parent.update_visuals()

  def destroy(self):
    self.shape_data = None
    self.parent.graphics = np.delete(self.parent.graphics, np.where(self.parent.graphics == self))



class Polygon(_Shape):
  def __init__(self, parent, shape_data, **kwargs):
    shape_contraint_text = "at least 3 points [x1, y1, x2, y2, x3, y3, ...]"
    super().__init__(parent, "polygon", shape_data, min_shape_data=6, shape_contraint_text=shape_contraint_text, **kwargs)

  def paint(self, p):
    p.beginPath()
    for i in range(0, len(self.shape_data), 2):
      x = self.shape_data[i] + self.parent.transform.position.x
      y = self.shape_data[i + 1] + self.parent.transform.position.y
      if i == 0:
        p.moveTo(x, y)
      else:
        p.lineTo(x, y)
    if self.fill:
      p.setFillStyle(self.fill)
      p.fill()
    if self.stroke:
      p.setStrokeStyle(self.stroke)
      p.stroke()
    p.closePath()

class Rectangle(_Shape):
  def __init__(self, parent, shape_data, **kwargs):
    shape_contraint_text = "4 element [x, y, width, height]"
    super().__init__(parent, "rectangle", shape_data, required_shape_data=4, shape_contraint_text=shape_contraint_text, **kwargs)
    self.rounded_corners = kwargs.get("rounded_corners", 0)

  def paint(self, p):
    rect = QRectF(
      self.shape_data[0] + self.parent.transform.position.x,
      self.shape_data[1] + self.parent.transform.position.y,
      self.shape_data[2],
      self.shape_data[3],
    )
    hole_rect = None
    if self.hole_rect is not None:
      hole_rect = QRectF(
        rect.left() + self.hole_rect[0],
        rect.top() + self.hole_rect[1],
        self.hole_rect[2],
        self.hole_rect[3]
      )
    p.beginPath()
    p.roundRect(rect, self.rounded_corners)
    if self.fill:
      p.setFillStyle(self.fill)
      if hole_rect is not None:
        p.beginHoleSubPath()
        p.roundRect(hole_rect, self.rounded_corners)
      p.fill()
    if self.stroke:
      p.setStrokeStyle(self.stroke)
      p.stroke()
    p.closePath()

class Oval(_Shape):
  def __init__(self, parent, shape_data, **kwargs):
    shape_contraint_text = "4 element [x, y, width, height]"
    super().__init__(parent, "oval", shape_data, required_shape_data=4, shape_contraint_text=shape_contraint_text, **kwargs)

  def paint(self, p):
    rect = QRectF(
      self.shape_data[0] + self.parent.transform.position.x,
      self.shape_data[1] + self.parent.transform.position.y,
      self.shape_data[2],
      self.shape_data[3],
    )
    p.beginPath()
    p.ellipse(rect)
    if self.fill:
      p.setFillStyle(self.fill)
      p.fill()
    if self.stroke:
      p.setStrokeStyle(self.stroke)
      p.stroke()
    p.closePath()

class Line(_Shape):
  def __init__(self, parent, shape_data, **kwargs):
    shape_contraint_text = "at least 2 points [x1, y1, x2, y2, ...]"
    super().__init__(parent, "line", shape_data, min_shape_data=4, shape_contraint_text=shape_contraint_text, **kwargs)

  def paint(self, p):
    p.beginPath()
    for i in range(0, len(self.shape_data), 2):
      x = self.shape_data[i] + self.parent.transform.position.x
      y = self.shape_data[i + 1] + self.parent.transform.position.y
      if i == 0:
        p.moveTo(x, y)
      else:
        p.lineTo(x, y)
    if self.stroke:
      p.setStrokeStyle(self.stroke)
      p.stroke()
    p.closePath()

# class Arc():
#   def __init__(self, parent, tags, x, y, width, height, **kwargs):
#     self.parent = parent
#     self.name = f"{__class__.__name__}_{id(self)}"

#     if width < 0:
#       raise ValueError("Width must be greater than 0")
#     if height < 0:
#       raise ValueError("Height must be greater than 0")

#     self.parent.canvas.create_arc(
#       x, y, x + width, y + height,
#       tags=[self.name, *tags],
#       **kwargs
#     )

