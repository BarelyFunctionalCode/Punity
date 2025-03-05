import numpy as np

class Transform:
  def __init__(self, object):
    self.object = object
    self._last_position = np.array([0, 0])

  @property
  def position(self):
    return np.array([self.object.root.winfo_x(), self.object.root.winfo_y()])

  @position.setter
  def position(self, new_position):
    self.object.root.update_idletasks()
    self._last_position = np.array(self.position)
    self.object.root.geometry(f"{self.width}x{self.height}+{new_position[0]}+{new_position[1]}")


  @property
  def last_position(self):
    return self._last_position


  @property
  def width(self):
    return self.object.root.winfo_width()
  

  @property
  def height(self):
    return self.object.root.winfo_height()