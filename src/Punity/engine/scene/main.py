import os
import signal
import sys
from PySide6.QtCore import QTimer
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt


# import platform
from Punity.engine import Environment, Object

from .border import Border
# from .editor import Editor

class Scene(Object):
  def __init__(self, dev_mode=False):
    os.environ['QT_QPA_PLATFORM'] = 'xcb'
    self.app = QApplication(sys.argv)
    Environment.update_screen()

    super().__init__(None, "root")
    # if platform.system() == 'Darwin':
    #   import AppKit
    #   # Set application activation policy to not allow menubar, dock, or application focus
    #   AppKit.NSApp.setActivationPolicy_(AppKit.NSApplicationActivationPolicyAccessory)


    self.editor = None
    Environment.set_root(self)
      
    # Environment.start_input_event_monitor()

    Border(self, Environment.width, Environment.height, Environment.x, Environment.y, 10)

    # Create the editor
    if dev_mode:
      Environment.dev_mode = True
      # self.editor = Editor(self, True)

    self._timer = QTimer(self.qt_obj)
    self._timer.timeout.connect(self._update)
    self._timer.start(10)

    # Method 1: Using QKeySequence string
    shortcut = QShortcut(QKeySequence("Ctrl+S"), self.qt_obj)
    shortcut.activated.connect(self.save_action)

    # Method 2: Using standard keys (platform-aware)
    standard_shortcut = QShortcut(QKeySequence.StandardKey.Save, self.qt_obj)
    standard_shortcut.activated.connect(self.save_action)

    # Method 3: Using Qt enumerations
    qt_shortcut = QShortcut(QKeySequence(Qt.CTRL | Qt.Key.Key_S), self.qt_obj)
    qt_shortcut.activated.connect(self.save_action)

  def save_action(self):
    print("Save triggered")


  def _update(self):
    for obj in self.children:
      obj._update()


  # Begins the main loop for the root object
  def begin(self):
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(self.app.exec())