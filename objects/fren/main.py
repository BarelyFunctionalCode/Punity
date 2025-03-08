import tkinter as tk
from queue import Queue

from .face import TkinterFace
from .terminal import TkinterTerminal

from ..object import Object
from components.movement import Movement
from components.rigidbody import Rigidbody

from utils import invis_tk

class Fren(Object, Movement, Rigidbody):
  def __init__(self, name, parent, x=0, y=0):
    # Initialize base Tkinter window
    root = invis_tk(tk.Toplevel(parent))
    root.title(name)
    root.geometry(f"200x200+{x}+{y}")

    root.update_idletasks()

    self.is_active = True
    self.is_waking_up = False
    self.inactivity_timer = 0
    self.inactivity_timeout = 2000
    self.terminal_despawn_timer = 0
    self.terminal_despawn_timeout = 5000

    self.face = TkinterFace(root)
    self.terminal = None
    self.terminal_update_queue = Queue()
    super().__init__(name, root, False)

  def start(self):
    super().start() if hasattr(super(), 'start') else None
    self.use_gravity = False
    self.set_face_expression("slow_scan")

    self.root.after(8000, lambda: self.enqueue_update_text("I make big shid, and I'm not sorry.\n\n\n💩"))

  def update(self):
    super().update() if hasattr(super(), 'update') else None
    if not hasattr(self, 'face'): return

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
        self.terminal.destroy()
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
          self.terminal = TkinterTerminal(self, self.terminal_update_queue, self.face.talking_queue)

    if self.face.is_asleep and self.move_mode != 'sleep':
      self.set_move_mode('sleep')

  # Used by the assistant to update the face parameters
  def enqueue_update_face(self, new_face_parameters, duration):
    self.face.update_queue.put((new_face_parameters, duration))

  # Used by the assistant to update the terminal text
  def enqueue_update_text(self, text):
    self.terminal_update_queue.put(text)
    if not self.terminal:
      self.terminal = TkinterTerminal(self, self.terminal_update_queue, self.face.talking_queue)

  # Used by the assistant to set the face expression
  def set_face_expression(self, expression):
    self.face.set_face_expression(expression)