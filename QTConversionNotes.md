# Needed Attributes

https://doc.qt.io/qtforpython-6/PySide6/QtGui/QWindow.html#PySide6.QtGui.QWindow.geometry
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QWindow.html#PySide6.QtGui.QWindow.setPosition
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QWindow.html#PySide6.QtGui.QWindow.startSystemMove
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QWindow.html#PySide6.QtGui.QWindow.startSystemResize

- x
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QWindow.html#PySide6.QtGui.QWindow.setX
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QWindow.html#id12

- y
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QWindow.html#PySide6.QtGui.QWindow.setY
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QWindow.html#id13

- width
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QWindow.html#PySide6.QtGui.QWindow.setWidth
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QWindow.html#id11

- height
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QWindow.html#PySide6.QtGui.QWindow.setHeight
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QWindow.html#id2

- background color
- alpha
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QWindow.html#PySide6.QtGui.QWindow.setOpacity
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QWindow.html#id8

- cursor
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QWindow.html#PySide6.QtGui.QWindow.setCursor


# Needed Functionality

- Object z-sorting
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QWindow.html#PySide6.QtGui.QWindow.lower
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QWindow.html#PySide6.QtGui.QWindow.raise

- Canvas with image and polygon drawing
https://doc.qt.io/qtforpython-6/examples/example_widgets_painting_basicdrawing.html#example-widgets-painting-basicdrawing
https://doc.qt.io/qtforpython-6/examples/example_gui_analogclock.html#example-gui-analogclock
https://doc.qt.io/qtforpython-6/examples/example_canvaspainter_hellowidget.html#example-canvaspainter-hellowidget
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QPixmap.html#PySide6.QtGui.QPixmap.setMask

- Modal functionality
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QWindow.html#PySide6.QtGui.QWindow.setModality

- Create windows with no toolbar and can be transparent with click-through
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QWindow.html#PySide6.QtGui.QWindow.setFlags
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QGuiApplication.html#PySide6.QtGui.QGuiApplication.quitOnLastWindowClosed
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QWindow.html#PySide6.QtGui.QWindow.setMask
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QPainter.html#PySide6.QtGui.QPainter.setBackgroundMode

Flags
Qt.FramelessWindowHint
Qt.WindowStaysOnTopHint
Qt::X11BypassWindowManagerHint
Qt.WindowTransparentForInput
Qt.WindowDoesNotAcceptFocus

- Some kind of loop

- Clipboard
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QGuiApplication.html#PySide6.QtGui.QGuiApplication.clipboard

- Color Scheme
https://doc.qt.io/qtforpython-6/PySide6/QtGui/QStyleHints.html#PySide6.QtGui.QStyleHints.colorScheme




# Files to Update

- [x] engine/object.py
- [x] engine/scene/main.py 
- [] engine/scene/editor/inspector.py
- [] engine/scene/editor/hierarchy.py
- [] engine/scene/editor/control_menu.py
- [x] engine/graphics/main.py
- [x] engine/graphics/text.py
- [] engine/graphics/sprite.py
- [] engine/graphics/shape.py
- [] engine/graphics/threedee/main.py
- [x] assets/effects/hole_punch.py (Abstract TK usage to object)
- [] assets/objects/terminal.py (Abstract TK usage to object)
- [x] assets/objects/screen_chunk.py
- [x] assets/objects/modal.py (Abstract TK usage to object)
- [x] assets/objects/hole.py (Abstract TK usage to object)
- [] assets/objects/fren/actions/hole_punch_entrance.py (Abstract TK usage to object)
- [x] assets/objects/toast/main.py


# Possible Changes

- Remove AppKit window property usage
- Replace usage of `setGeometry` and/or `setPosition` to `startSystemMove` and `startSystemResize`