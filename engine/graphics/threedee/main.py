import numpy as np
import tkinter as tk

from engine import Component, Environment
from engine.math import Vector3

class Triangle:
  def __init__(self, parent, vertices, color, tags=[]):
    self.parent = parent
    if len(vertices) != 3:
        raise ValueError("A triangle must have exactly 3 vertices.")
    if not isinstance(vertices[0], Vector3):
        vertices = [Vector3(v) for v in vertices]
    self.color = color
    self.tk_poly = None
    self.tags = tags
    self.z_index = 0
    self.vertices = vertices
    self.surface_normal = None

    self.draw_scale = 100

  def __repr__(self):
    return f"Triangle(\nz={self.z_index:.3f},\ncolor={self.color},\nsurface_normal={self.surface_normal}\n)"

  @property
  def vertices(self):
    return self._vertices
  
  @vertices.setter
  def vertices(self, value):
    if len(value) != 3:
        raise ValueError("A triangle must have exactly 3 vertices.")
    if not isinstance(value[0], Vector3):
        value = [Vector3(v) for v in value]
    self._vertices = value

  def draw(self):
    # multiply by the draw_scale to scale the vertices
    verts = [v * self.draw_scale for v in self._vertices]
    # offset vertices to center of the canvas
    canvas_offset = Vector3([
      self.parent.canvas.winfo_width() / 2,
      self.parent.canvas.winfo_height() / 2,
      0
    ])
    verts = [v + canvas_offset for v in verts]

    window_position = Vector3([
      self.parent.transform.position.x,
      self.parent.transform.position.y,
      0
    ])

    camera = Vector3([
       Environment.x + Environment.width / 2,
       Environment.y + Environment.height / 2,
       -500.0
    ])

    global_verts = [(window_position + v) - camera for v in verts]

    # perspective projection transformation
    global_verts = [
      Vector3([
        v.x * (490.0 / v.z),
        v.y * (490.0 / v.z),
        v.z
      ])
      for v in global_verts
    ]

    v1 = global_verts[1] - global_verts[0]
    v2 = global_verts[2] - global_verts[0]
    normal = Vector3.cross(v2, v1)
    self.surface_normal = normal.normalized

    self.z_index = float(np.mean([v.z for v in global_verts]))

    verts = [v + camera - window_position for v in global_verts]
    
    # Make the hex color closer to black the larger the self.z_index is
    brightness_factor = max(0, min(1, 1000 - self.z_index))
    color = self.color[1:]
    r, g, b = [int(color[i:i+2], 16) for i in (0, 2, 4)]
    r = int(r * brightness_factor)
    g = int(g * brightness_factor)
    b = int(b * brightness_factor)
    adjusted_color = f'#{r:02x}{g:02x}{b:02x}'

    is_culled = Vector3.dot(self.surface_normal, Vector3.forward) >= 0.0

    # offset_verts
    if self.tk_poly is None:
      points = [coord for vertex in verts for coord in (vertex.x, vertex.y)]
      self.tk_poly = self.parent.canvas.create_polygon(points, fill=adjusted_color, outline=adjusted_color, tags=self.tags)
    else:
      points = [coord for vertex in verts for coord in (vertex.x, vertex.y)]
      self.parent.canvas.coords(self.tk_poly, points)
      self.parent.canvas.tag_lower(self.tk_poly)
      self.parent.canvas.itemconfig(self.tk_poly, fill=adjusted_color, outline=adjusted_color)
      self.parent.canvas.itemconfig(self.tk_poly, state='hidden' if is_culled else 'normal')


  def update(self, vertices):
    if len(vertices) != 3:
        raise ValueError("A triangle must have exactly 3 vertices.")
    if not isinstance(vertices[0], Vector3):
        vertices = [Vector3(v) for v in vertices]
    self.vertices = vertices
    self.draw()

class Mesh(Component):
  def __init__(self, **kwargs):
    self.origin = kwargs.get('origin', Vector3.zero)
    self.vertices = np.array([Vector3(v) for v in kwargs.get('vertices', [])])
    self.triangles = []

    if not hasattr(self, "name"):
      self.name = ""

    self.tags = [self.name]
    if "tags" in kwargs:
      self.tags = [*self.tags, *list(kwargs["tags"])]
      del kwargs["tags"]

    if len(self.vertices) == 0:
      return
    
    if len(self.vertices) == 3:
      self.triangles = np.array([Triangle(self, self.vertices, '#FFFFFF', self.tags)])
    elif len(self.vertices) % 3 != 0:
      raise ValueError("Vertices must be a multiple of 3 for triangles.")
    elif len(self.vertices) < 3:
      raise ValueError("At least 3 vertices are required to form a triangle mesh.")
    elif len(self.vertices) % 3 == 0:
      self.triangles = np.array([
        Triangle(self, tri_verts, '#FFFFFF', self.tags)
        for tri_verts in np.array_split(self.vertices, len(self.vertices) // 3)
      ])

    if not hasattr(self, "canvas"):
      self.canvas = tk.Canvas(
        self.tk_obj,
        width=self.transform.width,
        height=self.transform.height,
        bg=self.tk_obj['bg'],
        bd=0,
        highlightthickness=0,
        cursor='none'
      )
      self.canvas.pack(padx=0, pady=0, side=tk.TOP)

    self.tk_obj.update_idletasks()

    self.color = kwargs.get('color', '#FFFFFF')
    
    self.draw()

    super().__init__(**kwargs)

  @property
  def color(self):
    return self._color
  
  @color.setter
  def color(self, value):
    self._color = value
    if isinstance(value, str):
      value = [value]
    color_grouping = len(self.triangles) // len(value)
    color_index = 0
    for i, triangle in enumerate(self.triangles):
      triangle.color = value[color_index]
      if (i + 1) % color_grouping == 0:
        color_index = (color_index + 1) % len(value)
    self.draw()

  def rotate(self, axis, angle):
    for triangle in self.triangles:
      triangle.vertices = [Vector3.rotate(v, self.origin, axis, angle) for v in triangle.vertices]

  def draw(self):
    # Sort numpy array of Triangle objects by z_index attribute
    tris = sorted(self.triangles, key=lambda t: t.z_index)
    for t in tris:
      t.draw()

  def update(self):
    super().update()
    self.draw()
    self.canvas.update_idletasks()