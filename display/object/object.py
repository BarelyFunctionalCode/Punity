from .transform import Transform

class Object:
  def __init__(self):
    super(Object, self).__init__()
    self._root = None

  @property
  def root(self):
    return self._root

  @root.setter
  def root(self, new_root):
    self._root = new_root
    self.transform = Transform(self)
    self._update()
    
  def _update(self):
    self.update()
    self.root.after(10, self._update)

  def update(self):
    print("base class")