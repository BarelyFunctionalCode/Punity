from PySide6.QtWidgets import QTextEdit
from PySide6.QtCore import Qt

from engine.object import Object  


class InputBox(Object):
  def __init__(self, parent: Object, width, height, x, y, color="white"):

    self.color = color
    self.text_edit = None
    super().__init__(parent, "inputBox", width, height, x, y)
    self.last_position = self.transform.position

  @property
  def text(self):
    if self.text_edit is not None:
      return self.text_edit.toPlainText()
    return ""


  def update(self):
    super().update()

    # position = self.transform.position
    # if self.text_edit is not None:
    #   if Vector2.distance(self.last_position, position) > 0:
    #     self.text_edit.setGeometry(position.x, position.y, self.transform.width, self.transform.height)
    # self.last_position = position

  def show(self):
    position = self.transform.position
    self.text_edit = QTextEdit(self.parent.qt_obj)
    self.text_edit.setAttribute(Qt.WA_TranslucentBackground)
    self.text_edit.setStyleSheet(f"background: transparent; color: {self.color};")
    self.text_edit.show()
    self.text_edit.setGeometry(position.x, position.y, self.transform.width, self.transform.height)
    self.text_edit.setFocus()

  def hide(self):
    if self.text_edit is not None:
      self.text_edit.clearFocus()
      self.text_edit.close()
      self.text_edit = None