class Component:
  def __init__(self, **kwargs):
    super().__init__()

  def start(self):
    Exception("Not Implemented")

  def update(self):
    Exception("Not Implemented")

  def on_collision(self, col_normal, col_vec, other_object):
    Exception("Not Implemented")