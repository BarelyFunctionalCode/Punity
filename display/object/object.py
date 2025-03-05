from .transform import Transform

class Object:
  def __init__(self, root):
    self.root = root
    self.transform = Transform(self)
    super().__init__()

    self._update()
    
  def _update(self):
    if self.root == None: return
    self.update()
    self.root.after(10, self._update)

  def update(self):
    super().update() if hasattr(super(), 'update') else None