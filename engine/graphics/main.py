import subprocess
from PySide6.QtCore import QRect, Qt, Signal, Slot
from PySide6.QtGui import QColorConstants
from PySide6.QtCanvasPainter import (QCanvasPainterWidget)
import numpy as np

from engine import Environment


class QTWindow(QCanvasPainterWidget):
  set_inputs_signal = Signal(bool)
  
  def __init__(self, _object):
    self.object = _object
    super().__init__(None)
    self.set_inputs_signal.connect(self._set_inputs)

    self.is_input_enabled = False

    self.setWindowFlag(Qt.Tool)
    self.setWindowFlag(Qt.WindowStaysOnTopHint)
    self.setWindowFlag(Qt.WindowTransparentForInput)
    self.setWindowFlag(Qt.FramelessWindowHint)
    self.setAttribute(Qt.WA_TranslucentBackground)

    subprocess.check_call([
      "xprop",
      "-f", "_NET_WM_STATE", "32a",
      "-id", str(self.winId()),
      "-set", "_NET_WM_STATE", "_NET_WM_STATE_SKIP_TASKBAR",
    ])
    
    self.setGeometry(
      Environment.x + Environment.x_offset,
      Environment.y + Environment.y_offset,
      Environment.width,
      Environment.height
    )
    
    self.m_image = None
    self.setFillColor(QColorConstants.Transparent)
    self.show()

  def paint(self, p):
    for child in self.object.children:
      child.paint(p)


  def set_inputs(self, enabled):
    self.set_inputs_signal.emit(enabled)
  @Slot(bool)
  def _set_inputs(self, enabled):
    if enabled == self.is_input_enabled:
      return
    self.setWindowFlag(Qt.WindowTransparentForInput, not enabled)
    subprocess.check_call([
      "xprop",
      "-f", "_NET_WM_STATE", "32a",
      "-id", str(self.winId()),
      "-set", "_NET_WM_STATE", "_NET_WM_STATE_SKIP_TASKBAR",
    ])
    self.show()
    if enabled:
      self.activateWindow()
    self.is_input_enabled = enabled

  def mouseReleaseEvent(self, event):
    # Propagate the mouse release event to child objects
    for target in reversed(self.object.children):
      done = target._mouse_event(event)
      if done:
        break

class Graphic:
  def __init__(self, parent, name="graphic"):
    self.parent = parent
    self.name = f"{name.lower()}_{id(self)}"

    if self.parent is not None:
      self.parent.graphics = np.append(self.parent.graphics, self)

  def destroy(self):
    if self.parent is not None:
      self.parent.graphics = np.delete(self.parent.graphics, np.where(self.parent.graphics == self))
      self.parent.update_visuals()
      self.parent = None