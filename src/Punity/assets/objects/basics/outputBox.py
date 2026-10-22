import re
from turtle import color
from PySide6.QtWidgets import QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from Punity.engine.object import Object  


class OutputBox(Object):
  def __init__(self, parent: Object, width, height, x, y, font_size=16, fill="white", opacity=1.0):

    self.text_edit = None
    self._text = ""
    super().__init__(parent, "outputBox", width, height, x, y)

    self.default_styles = """
    padding: 0;
    margin: 0;
    background-color: rgba(255, 255, 255, 0);
    """
    self.styles = {}

    self.font_size = font_size
    self.fill = fill
    self.opacity = opacity
    self.last_position = self.transform.position

  @property
  def text(self):
    return self._text

  @property
  def font_size(self):
    return self.styles.get("font-size")
  
  # @property
  # def fill(self):
  #   return self.styles.get("color")

  @property
  def opacity(self):
    return self.styles.get("opacity")

  
  @text.setter
  def text(self, value):
    if self.text_edit is not None and value != self._text:
      # self.text_edit.setPlainText(value)
      # text is in form "some text <!{COLOR}!>some text some text <!{COLOR}!>some text some text <!{COLOR}!>some text"
      parts = re.split(r"(<!.*?!>)", value)
      self.text_edit.clear()
      self.text_edit.setTextBackgroundColor(QColor(0,0,0,0))
      for p in parts:
        if p[0:2] == "<!":
            match = re.match(r"<!(.*?)!>", p)
            if match != None:
              self.text_edit.setTextBackgroundColor(QColor(match.group(1)))
        else:
          cursor = self.text_edit.textCursor()
          cursor.insertText(p)
      self.text_edit.setTextBackgroundColor(QColor(0,0,0,0))
      self._text = value

  @font_size.setter
  def font_size(self, value):
    value = f"{max(value, 1)}px"
    if self.text_edit is not None and self.font_size != value:
      self.setStyle("font-size", value)

  # @fill.setter
  # def fill(self, value):
  #   if self.text_edit is not None and self.fill != value:
  #     self.setStyle("color", value)

  @opacity.setter
  def opacity(self, value):
    value = min(max(value, 0.0), 1.0)
    if self.text_edit is not None and self.opacity != value:
      self.setStyle("opacity", value)


  def setStyle(self, key, value):
    self.styles[key] = value
    if self.text_edit is not None:
      style_str = "; ".join(f"{k}: {v}" for k, v in self.styles.items())
      self.text_edit.setStyleSheet(self.default_styles + style_str)

  def start(self):
    super().start()

    position = self.transform.position
    self.text_edit = QTextEdit(self.parent.qt_obj)
    self.text_edit.setReadOnly(True)
    self.text_edit.setAttribute(Qt.WA_TranslucentBackground)
    self.text_edit.show()
    self.text_edit.setGeometry(position.x, position.y, self.transform.width, self.transform.height)

  def post_update(self, did_geomentry_update):
    super().post_update(did_geomentry_update)

    if did_geomentry_update and self.text_edit is not None:
      position = self.transform.position
      self.text_edit.setGeometry(position.x, position.y, self.transform.width, self.transform.height)

