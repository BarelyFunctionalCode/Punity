import numpy as np
import time

from engine import Environment

from engine import Object
from engine.graphics import Mesh
from engine.math import Vector2
from engine.math import Vector3

class Cube(Object, Mesh):
  def __init__(self, parent, **kwargs):
    # Cube vertices
    vertices=[
      [0, 0, 0], # Front, bottom-left triangle
      [1, 1, 0],
      [0, 1, 0],
      [0, 0, 0], # Front, top-right triangle
      [1, 0, 0],
      [1, 1, 0],
      [0, 1, 1], # Back, bottom-left triangle
      [1, 1, 1],
      [0, 0, 1], 
      [1, 1, 1], # Back, top-right triangle
      [1, 0, 1],
      [0, 0, 1], 
      [0, 1, 0], # Left, bottom-left triangle
      [0, 1, 1],
      [0, 0, 0], 
      [0, 0, 0], # Left, top-right triangle
      [0, 1, 1],
      [0, 0, 1],
      [1, 0, 0], # Right, bottom-left triangle
      [1, 1, 1],
      [1, 1, 0],
      [1, 0, 1], # Right, top-right triangle
      [1, 1, 1],
      [1, 0, 0], 
      [0, 0, 0], # Bottom, bottom-left triangle
      [1, 0, 1],
      [1, 0, 0],
      [0, 0, 1], # Bottom, top-right triangle
      [1, 0, 1],
      [0, 0, 0], 
      [1, 1, 0], # Top, bottom-left triangle
      [1, 1, 1],
      [0, 1, 0], 
      [0, 1, 0], # Top, top-right triangle
      [1, 1, 1],
      [0, 1, 1]
    ]
    kwargs = {
      'vertices': vertices,
      'origin': Vector3([0.5, 0.5, 0.5]),
      'color': ['#FF0000', "#FFFF00", '#00FF00', '#00FFFF', '#0000FF', '#FF00FF'],
    }
    super().__init__(parent, 'Cube', 300, 300, 400, 200, False, **kwargs)

    self.rotate(Vector3.left, 0.8)

  def update(self):
    super().update()

    # Adjust position to go in a circle around the center of the screen
    self.transform.position = Vector2([
      Environment.width / 2 + (300 * np.cos(time.time() * 0.9)) - 150,
      Environment.height / 2 + (300 * np.sin(time.time() * 0.9)) - 150
    ])

    # Rotate the Cube around the y-axis
    self.rotate(Vector3.up, 0.02)

    # Rainbow changing hex color
    # color = self.color[1:]
    # color = [int(color[i:i+2], 16) for i in (0, 2, 4)]
    # color[0] = (color[0] + 1) % 256
    # color[1] = (color[1] + 2) % 256
    # color[2] = (color[2] + 3) % 256
    # self.color = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])