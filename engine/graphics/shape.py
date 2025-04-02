import tkinter as tk


class _Shape():
  def __init__(self, parent, points, min_points=0, required_points=0, **kwargs):
    self.parent = parent
    self.name = f"{__class__.__name__}_{id(self)}"

    if type(points) not in [list, tuple] or len(points) % 2 != 0 or len(points) < min_points or len(points) < required_points:
      point_contraint_text = f"at least {min_points}" if min_points > 0 else f"exactly {required_points}"
      raise ValueError(f"points must be a list [x1, y1, x2, y2 ...] with {point_contraint_text} elements\n\npoints: {points}")
    
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

  def bind(self, event, callback):
    self.parent.canvas.tag_bind(self.name, event, callback)
    
  def unbind(self, event):
    self.parent.canvas.tag_unbind(self.name, event)
  
  def update(self, points):
    self.parent.canvas.coords(self.name, points)

  def destroy(self):
    self.parent.canvas.delete(self.name)
    



class Polygon(_Shape):
  def __init__(self, parent, points, *args, **kwargs):
    super().__init__(parent, points, min_points=6, **kwargs)

    self.parent.canvas.create_polygon(
      points,
      *args,
      tags=self.tags,
      **kwargs
    )

class Rectangle(_Shape):
  def __init__(self, parent, points, *args, **kwargs):
    super().__init__(parent, points, required_points=4, **kwargs)

    self.parent.canvas.create_rectangle(
      points,
      *args,
      tags=self.tags,
      **kwargs
    )

class Oval(_Shape):
  def __init__(self, parent, points, *args, **kwargs):
    super().__init__(parent, points, required_points=4, **kwargs)

    self.parent.canvas.create_oval(
      points,
      *args,
      tags=self.tags,
      **kwargs
    )

class Line(_Shape):
  def __init__(self, parent, points, *args, **kwargs):
    super().__init__(parent, points, min_points=4, **kwargs)

    self.parent.canvas.create_line(
      points,
      *args,
      tags=self.tags,
      **kwargs
    )

# class Arc():
#   def __init__(self, parent, tags, x, y, width, height, **kwargs):
#     self.parent = parent
#     self.name = f"{__class__.__name__}_{id(self)}"

#     if width < 0:
#       raise ValueError("Width must be greater than 0")
#     if height < 0:
#       raise ValueError("Height must be greater than 0")

#     self.parent.canvas.create_arc(
#       x, y, x + width, y + height,
#       tags=[self.name, *tags],
#       **kwargs
#     )

