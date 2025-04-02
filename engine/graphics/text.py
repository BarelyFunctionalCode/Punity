import tkinter as tk

class Text:
  def __init__(self, parent, text, x, y, **kwargs):
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

    self.parent.canvas.create_text(
      x, y,
      text=text,
      tags=self.tags,
      **kwargs
    )

  def bind(self, event, callback):
    self.parent.canvas.tag_bind(self.name, event, callback)
    
  def unbind(self, event):
    self.parent.canvas.tag_unbind(self.name, event)

  def update(self, text):
    self.parent.canvas.itemconfig(self.name, text=text)

  def destroy(self):
    self.parent.canvas.delete(self.name)