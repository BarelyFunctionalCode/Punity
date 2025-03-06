import tkinter as tk
import platform

from .face import TkinterFace
from .terminal import TkinterTerminal

from components.object import Object
from components.movement import Movement
from components.rigidbody import Rigidbody

from utils import invis_tk

class Display(Object, Movement, Rigidbody):
  def __init__(self, name, parent):
    # Initialize base Tkinter window
    root = invis_tk(tk.Toplevel(parent))
    root.title(name)
    root.geometry("200x200+100+100")

    root.update_idletasks()

    super().__init__(name, root, False)

    self.is_active = True
    self.is_waking_up = False
    self.inactivity_timer = 0
    self.inactivity_timeout = 100

    self.face = TkinterFace(self.root)
    # self.terminal = TkinterTerminal(self.root, self.face.talking_queue)

  def update(self):
    super().update() if hasattr(super(), 'update') else None
    if not hasattr(self, 'face'): return

    if self.face.is_active:
    # if self.face.is_active or self.terminal.is_active:
      self.inactivity_timer = 0

    if self.is_active and not self.face.is_active:
    # if self.is_active and not self.face.is_active and not self.terminal.is_active:
      self.inactivity_timer += 1
      if self.inactivity_timer > self.inactivity_timeout:
        self.is_active = False
        self.face.set_face_expression("sleep")
        # self.terminal.set_enabled(False)

    if not self.is_active and not self.is_waking_up and self.inactivity_timer < self.inactivity_timeout:
      self.face.set_face_expression("wake")
      self.is_waking_up = True
    elif self.is_waking_up:
      if self.face.is_enabled:
        self.is_active = True
        self.is_waking_up = False
        # self.terminal.set_enabled(True)

    if self.face.is_asleep and self.move_mode != 'sleep':
      self.set_move_mode('sleep')

  # Used by the assistant to update the face parameters
  def enqueue_update_face(self, new_face_parameters, duration):
    self.face.update_queue.put((new_face_parameters, duration))

  # Used by the assistant to update the terminal text
  def enqueue_update_text(self, text):
    self.terminal.update_queue.put(text)

  # Used by the assistant to set the face expression
  def set_face_expression(self, expression):
    self.face.set_face_expression(expression)