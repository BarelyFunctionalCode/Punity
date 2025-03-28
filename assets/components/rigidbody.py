from engine import Component
from engine.math import Vector2


GRAVITY = 3

class Rigidbody(Component):
  def __init__(self):
    self.use_gravity = True
    self.velocity = Vector2.zero
    self.acceleration = Vector2.zero
    self.drag = 0.05
    self.max_speed = 100
    self.mass = 1
    self.bounciness = 1.0
    self.gravity_modifier = 1.0
    super().__init__()

  def start(self):
    super().start()
    self.collision_enabled = True

  # Basic Physics Simulation
  def update(self):
    super().update()
    # Gravity constant acceleration
    if self.use_gravity:
      self.acceleration += Vector2.down * GRAVITY * self.gravity_modifier

    # Calculate velocity based off of acceleration and drag
    self.velocity += self.acceleration
    self.velocity -= self.velocity * self.drag
    self.velocity = Vector2.clamp_magnitude(self.velocity, self.max_speed)
    self.transform.position += self.velocity

    self.acceleration = Vector2.zero

  # Physics response to collisions
  def on_collision(self, col_normal, _col_vec, _other_object):
    # TODO: Need to take into account the other object's velocity
    super().on_collision(col_normal, _col_vec, _other_object)
    self.velocity = Vector2.reflect(self.velocity, col_normal) * self.bounciness

  # Apply a force to the object (acceleration = force / mass)
  def apply_force(self, force):
    self.acceleration += force / self.mass