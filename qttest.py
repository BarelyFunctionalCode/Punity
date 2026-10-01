import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class TransparentWindow(QWidget):
  def __init__(self):
    super().__init__()
    
    # 1. Remove window frame
    self.setWindowFlags(Qt.FramelessWindowHint)
    
    # 2. Enable translucent background
    self.setAttribute(Qt.WA_TranslucentBackground)
    
    # 3. Add content (this remains opaque)
    layout = QVBoxLayout(self)
    label = QLabel("Hello, Transparent World!")
    layout.addWidget(label)
    
    self.resize(400, 300)

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = TransparentWindow()
  window.show()
  sys.exit(app.exec())   