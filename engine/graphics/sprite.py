from PIL import ImageQt
import numpy as np
from PySide6.QtGui import QColor


class Sprite:
  def __init__(self, parent, image, x, y, **kwargs):
    self.parent = parent
    self.name = f"{__class__.__name__}_{id(self)}"

    # Required for MacOS. Essentially puts a black background behind the image, otherwise the image will be transparent
    # Load the image
    # buf = io.BytesIO()
    # image.save(buf, format="PNG")
    # cvimg = cv2.imdecode(np.frombuffer(buf.getvalue(), np.uint8), cv2.IMREAD_UNCHANGED)

    # # Get binary alpha mask
    # _, cvmask = cv2.threshold(cvimg[:, :, 3], 0, 255, cv2.THRESH_BINARY)

    # # Find contours
    # contours, _ = cv2.findContours(cvmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # # Draw contours as polygons
    # for contour in contours:
    #   # Simplify the contour
    #   epsilon = 0.005 * cv2.arcLength(contour, True)
    #   contour = cv2.approxPolyDP(contour, epsilon, True)
    #   contour = contour.flatten().tolist()
    #   self.parent.canvas.create_polygon(contour, fill='black', outline='black', width=1, tags=[f"{self.name}_mask"])
    # buf.close()

    self._tint_color = None
    self._opacity = 1.0
    
    self.x = x
    self.y = y
    self.img = ImageQt.ImageQt(image)

    self.tint_color = kwargs.get("tint_color", "#ffffff")
    self.opacity = kwargs.get("opacity", 1.0)

    self.parent.graphics = np.append(self.parent.graphics, self)

  @property
  def tint_color(self):
    return self._tint_color

  @property
  def opacity(self):
    return self._opacity
  
  @tint_color.setter
  def tint_color(self, value):
    old_tint_color = self._tint_color
    self._tint_color = QColor(value)
    self._tint_color.setAlphaF(self._opacity)
    if old_tint_color != self._tint_color:
      self.parent.update_visuals()

  @opacity.setter
  def opacity(self, value):
    value = min(max(value, 0.0), 1.0)
    if value == self._opacity:
      return
    self._opacity = value
    if self._tint_color is not None:
      self._tint_color.setAlphaF(self._opacity)
    self.parent.update_visuals()

  def paint(self, p):
    if self.img is not None:
      img = p.addImage(self.img)
      img.setTintColor(self.tint_color.name())
      position = self.parent.transform.position
      p.drawImage(img, self.x + position.x, self.y + position.y)

  def update(self, image, x=None, y=None):
    self.img = ImageQt.ImageQt(image)
    if x is not None:
      self.x = x
    if y is not None:
      self.y = y
    self.parent.update_visuals()

  def destroy(self):
    del self.img
    self.parent.update_visuals()