import tkinter as tk
from PIL import ImageTk
import cv2
import numpy as np
import io

class Sprite:
  def __init__(self, parent, image, x, y, **kwargs):
    self.parent = parent
    self.name = f"{__class__.__name__}_{id(self)}"

    if not hasattr(self.parent, "canvas"):
      self.parent.canvas = tk.Canvas(
        self.parent.tk_obj,
        width=self.parent.transform.width,
        height=self.parent.transform.height,
        bg=self.parent.tk_obj['bg'],
        bd=0,
        highlightthickness=0,
        cursor='none'
      )
      self.parent.canvas.pack(padx=0, pady=0, side=tk.TOP)

    self.tags = [self.name]
    if "tags" in kwargs:
      self.tags = [*self.tags, *list(kwargs["tags"])]
      del kwargs["tags"]

    # Required for MacOS. Essentially puts a black background behind the image, otherwise the image will be transparent
    # Load the image
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    cvimg = cv2.imdecode(np.frombuffer(buf.getvalue(), np.uint8), cv2.IMREAD_UNCHANGED)

    # Get binary alpha mask
    _, cvmask = cv2.threshold(cvimg[:, :, 3], 0, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(cvmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours as polygons
    for contour in contours:
      # Simplify the contour
      epsilon = 0.005 * cv2.arcLength(contour, True)
      contour = cv2.approxPolyDP(contour, epsilon, True)
      contour = contour.flatten().tolist()
      self.parent.canvas.create_polygon(contour, fill='black', outline='black', width=1, tags=[f"{self.name}_mask"])
    buf.close()
    

    self.parent.images[self.name] = ImageTk.PhotoImage(image)
    self.parent.canvas.create_image(
      x, y,
      image=self.parent.images[self.name],
      tags=self.tags,
      **kwargs
    )

  def update(self, image, x=None, y=None):
    self.img = ImageTk.PhotoImage(image)
    self.parent.canvas.itemconfig(self.name, image=self.img)

    if x or y:
      self.parent.canvas.coords(self.name, x, y)
      self.parent.canvas.coords(f"{self.name}_mask", x, y)

  def destroy(self):
    self.parent.canvas.delete(self.name)