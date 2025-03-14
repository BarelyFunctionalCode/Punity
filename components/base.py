class Base:
  def __init__(self):
    super().__init__()

  def start(self):
    Exception("Not Implemented")

  def update(self):
    Exception("Not Implemented")

  def on_collision(self, col_normal, _col_vec, _other_object):
    Exception("Not Implemented")