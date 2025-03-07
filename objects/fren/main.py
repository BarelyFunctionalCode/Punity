import tkinter as tk
from queue import Queue

from .face import TkinterFace
from .terminal import TkinterTerminal

from ..object import Object
from components.movement import Movement
from components.rigidbody import Rigidbody

from utils import invis_tk

class Fren(Object, Movement, Rigidbody):
  def __init__(self, name, parent):
    # Initialize base Tkinter window
    root = invis_tk(tk.Toplevel(parent))
    root.title(name)
    root.geometry("200x200+100+100")

    root.update_idletasks()

    self.is_active = True
    self.is_waking_up = False
    self.inactivity_timer = 0
    self.inactivity_timeout = 5000
    self.terminal_despawn_time = 500

    self.face = TkinterFace(root)
    self.terminal = None
    self.terminal_update_queue = Queue()
    super().__init__(name, root, False)

  def start(self):
    self.set_face_expression("slow_scan")

    self.root.after(2000, lambda: self.enqueue_update_text("Hello! I'm Fren, your personal assistant!"))

  def update(self):
    super().update() if hasattr(super(), 'update') else None
    if not hasattr(self, 'face'): return

    # if self.face.is_active:
    if self.face.is_active or (self.terminal and self.terminal.is_active):
      self.inactivity_timer = 0

    # if self.is_active and not self.face.is_active:
    if self.is_active and not self.face.is_active and (not self.terminal or (self.terminal and not self.terminal.is_active)):
      self.inactivity_timer += 1

      if self.terminal and self.inactivity_timer > self.terminal_despawn_time:
        self.terminal.destroy()
        self.terminal = None
      if not self.terminal and self.inactivity_timer > self.inactivity_timeout:
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
        if not self.terminal and not self.terminal_update_queue.empty():
          self.terminal = TkinterTerminal(self, self.terminal_update_queue, self.face.talking_queue)
        # self.terminal.set_enabled(True)

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