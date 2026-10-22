import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
import signal
from PySide6.QtCore import Qt

import subprocess

class TransparentWindow(QWidget):
  def __init__(self):
    super().__init__()
    
    self.setWindowFlag(Qt.WindowStaysOnTopHint)
    self.setWindowFlag(Qt.FramelessWindowHint)
    self.setWindowFlag(Qt.WindowTransparentForInput)
    self.setWindowFlag(Qt.WindowDoesNotAcceptFocus)
    
    # self.setAttribute(Qt.WA_X11NetWmWindowTypeDesktop)

    subprocess.check_call([
      "xprop",
      "-f", "_NET_WM_STATE", "32a",
      "-id", str(self.winId()),
      "-set", "_NET_WM_STATE", "_NET_WM_STATE_SKIP_TASKBAR",
    ])
    
    # 3. Add content (this remains opaque)
    layout = QVBoxLayout(self)
    label = QLabel("Hello, Transparent World!")
    layout.addWidget(label)
    
    self.resize(400, 300)

if __name__ == "__main__":
  os.environ['QT_QPA_PLATFORM'] = 'xcb'
  QApplication.setAttribute(Qt.AA_DontShowIconsInMenus)
  QApplication.setAttribute(Qt.AA_DontShowShortcutsInContextMenus)
  QApplication.setAttribute(Qt.AA_PluginApplication)
  app = QApplication(sys.argv)
  window = TransparentWindow()
  window.show()
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  sys.exit(app.exec())   