from PySide6.QtCanvasPainter import (QCanvasPainter)
import numpy as np
from PySide6.QtGui import QColor, QFont

from engine.graphics.main import Graphic


class Text(Graphic):
  text_alignments = {
    "left": QCanvasPainter.TextAlign.Left,
    "center": QCanvasPainter.TextAlign.Center,
    "right": QCanvasPainter.TextAlign.Right
  }
  text_baselines = {
    "top": QCanvasPainter.TextBaseline.Top,
    "middle": QCanvasPainter.TextBaseline.Middle,
    "bottom": QCanvasPainter.TextBaseline.Bottom,
    "hanging": QCanvasPainter.TextBaseline.Hanging
  }

  def __init__(self, parent, text, **kwargs):
    self._fill = None
    self._opacity = 1.0
    self._text = ""

    super().__init__(parent, "text")

    self.text = text
    self.x = kwargs.get("x", parent.transform.width / 2)
    self.y = kwargs.get("y", parent.transform.height / 2)
    self.font_size = kwargs.get("font_size", 20)
    self.fill = kwargs.get("fill", "black")
    self.opacity = kwargs.get("opacity", 1.0)
    self.max_width = kwargs.get("max_width", parent.transform.width)
    self.text_align = kwargs.get("text_align", QCanvasPainter.TextAlign.Center)
    self.text_baseline = kwargs.get("text_baseline", QCanvasPainter.TextBaseline.Middle)


  @property
  def fill(self):
    return self._fill

  @property
  def opacity(self):
    return self._opacity

  @property
  def text(self):
    return self._text

  @fill.setter
  def fill(self, value):
    old_fill = self._fill
    self._fill = QColor(value)
    self._fill.setAlphaF(self._opacity)
    if old_fill != self._fill:
      self.parent.update_visuals()

  @opacity.setter
  def opacity(self, value):
    value = min(max(value, 0.0), 1.0)
    if value == self._opacity:
      return
    self._opacity = value
    self._fill.setAlphaF(self._opacity)
    self.parent.update_visuals()

  @text.setter
  def text(self, value):
    if value == self._text:
      return
    self._text = value
    self.parent.update_visuals()

  def paint(self, p):
    if self.text is None:
      return

    font_size = round(self.font_size)
    if font_size > 0:
      p.setTextAlign(self.text_align)
      p.setTextBaseline(self.text_baseline)
      # font1.setWeight(QFont.Weight.Bold)
      font1 = QFont("VCR OSD Mono")
      font1.setPixelSize(font_size)
      p.setFont(font1)
      p.setFillStyle(self.fill)
      p.setTextWrapMode(QCanvasPainter.WrapMode.Wrap)
      position = self.parent.transform.position
      p.fillText(self.text, position.x + self.x, position.y + self.y, self.max_width)