from queue import Queue

from .face import TkinterFace
from ..terminal import Terminal

from ..object import Object
from components.movement import Movement
from components.rigidbody import Rigidbody
from utils import Vector2

from . import actions

class Fren(Object, Movement, Rigidbody):
  def __init__(self, parent, entrance=None):
    self.face_polygon = [20,0, 120,0, 140,20, 145,90, 120,140, 90,160, 50,160, 20,140, -5,90, 0,20, 20,0,]
    x = 200
    y = 200
    self.entrance = None
    if entrance in actions.entrances:
      self.entrance = actions.entrances[entrance]
      x = self.entrance.spawn_position.x
      y = self.entrance.spawn_position.y

    self.is_active = True
    self.is_waking_up = False
    self.inactivity_timer = 0
    self.inactivity_timeout = 2000
    self.terminal_despawn_timer = 0
    self.terminal_despawn_timeout = 5000
    self.terminal = None
    self.terminal_update_queue = Queue()
    self.face = None
    super().__init__(parent, 'fren', 140, 170, x, y, False)
    
  def start(self):
    super().start()
    self.use_gravity = False

    self.face = TkinterFace(self, [20,0, 120,0, 140,20, 145,90, 120,140, 90,160, 50,160, 20,140, -5,90, 0,20, 20,0,])

    if self.entrance:
      self.entrance = self.entrance(self.parent, self)

    self.tk_obj.after(12000, lambda: self.enqueue_update_text("I make big shid, and I'm not sorry.\n\n\n💩"))


  def update(self):
    super().update()
    if not hasattr(self, 'face'): return

    self.face.update()

    if self.terminal and self.terminal.is_destroyed:
      self.terminal = None
    if self.terminal and self.terminal.is_active:
      self.terminal_despawn_timer = 0
    if self.face.is_active:
      self.inactivity_timer = 0

    if self.is_active:
      if self.terminal and not self.terminal.is_active:
        self.terminal_despawn_timer += self.delta_time
      if not self.terminal and not self.face.is_active:
        self.inactivity_timer += self.delta_time

      if self.terminal and self.terminal_despawn_timer > self.terminal_despawn_timeout:
        self.terminal.start_destroy()
      if not self.terminal and self.inactivity_timer > self.inactivity_timeout:
        self.is_active = False
        self.face.set_face_expression("sleep")

    if not self.is_active and not self.is_waking_up and self.inactivity_timer < self.inactivity_timeout:
      self.face.set_face_expression("wake")
      self.is_waking_up = True
    elif self.is_waking_up:
      if self.face.is_enabled:
        self.is_active = True
        self.is_waking_up = False
        if not self.terminal and not self.terminal_update_queue.empty():
          terminal_position = self.transform.position.astype(int) - Vector2([0, 100])
          self.terminal = Terminal(self, terminal_position.x, terminal_position.y, self.terminal_update_queue, self.face.talking_queue)

    if self.face.is_asleep and self.move_mode != 'sleep':
      self.set_move_mode('sleep')

  # Used by the assistant to update the face parameters
  def enqueue_update_face(self, new_face_parameters, duration):
    self.face.update_queue.put((new_face_parameters, duration))

  # Used by the assistant to update the terminal text
  def enqueue_update_text(self, text):
    self.terminal_update_queue.put(text)
    if not self.terminal:
      terminal_position = self.transform.position.astype(int) - Vector2([0, 100])
      self.terminal = Terminal(self, terminal_position.x, terminal_position.y, self.terminal_update_queue, self.face.talking_queue)

  # Used by the assistant to set the face expression
  def set_face_expression(self, expression):
    self.face.set_face_expression(expression)