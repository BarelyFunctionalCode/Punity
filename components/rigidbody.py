from utils import Vector2

GRAVITY = 3

class Rigidbody:
  def __init__(self):
    super().__init__()
    self.use_gravity = True
    self.velocity = Vector2.zero
    self.acceleration = Vector2.zero
    self.drag = 0.05
    self.max_speed = 100
    self.mass = 1
    self.bounciness = 1.0

  def update(self):
    super().update() if hasattr(super(), 'update') else None

    if self.use_gravity:
      self.acceleration += Vector2.down * GRAVITY

    self.velocity += self.acceleration
    self.velocity -= self.velocity * self.drag
    self.velocity = Vector2.clamp_magnitude(self.velocity, self.max_speed)

    self.transform.position += self.velocity

    self.acceleration = Vector2.zero

  def on_collision(self, col_normal, _col_vec, _other_object):
    super().on_collision(col_normal, _col_vec, _other_object) if hasattr(super(), 'on_collision') else None
    self.velocity = Vector2.reflect(self.velocity, col_normal) * self.bounciness

  def apply_force(self, force):
    self.acceleration += force / self.mass