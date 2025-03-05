import tkinter as tk
import numpy as np

from .face import TkinterFace
from .terminal import TkinterTerminal

from .object.object import Object

from .movement import Movement

class Display(Object, Movement):
  def __init__(self):
    super(Display, self).__init__()
    # Initialize base Tkinter window and the face and terminal objects
    self.root = tk.Tk()
    self.root.title("Face")
    self.root.geometry("200x200+100+100")
    self.root.config(cursor='none', bg='black')

    self.root.overrideredirect(True)
    self.root.lift()
    self.root.wm_attributes("-topmost", True)
    self.root.wm_attributes("-disabled", True)
    self.root.wm_attributes("-transparentcolor", "black")

    self.is_active = True
    self.is_waking_up = False
    self.inactivity_timer = 0
    self.inactivity_timeout = 500

    self.face = TkinterFace(self.root)
    # self.terminal = TkinterTerminal(self.root, self.face.talking_queue)

  def stop(self):
    # Stop the Tkinter main loop
    self.root.destroy()
    self.root = None

  def start(self):
    # Start the Tkinter main loop
    self.root.bind_all("<Control-c>", lambda e: self.stop())
    self.root.mainloop()
    
  def update(self):
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
      
    # Update the display window position if needed
    new_movement = self.check_for_movement(self.transform)
    if not np.array_equal(new_movement, np.zeros(2)):
      self.transform.position = self.transform.position + new_movement

  # Used by the assistant to update the face parameters
  def enqueue_update_face(self, new_face_parameters, duration):
    self.face.update_queue.put((new_face_parameters, duration))

  # Used by the assistant to update the terminal text
  def enqueue_update_text(self, text):
    self.terminal.update_queue.put(text)

  # Used by the assistant to set the face expression
  def set_face_expression(self, expression):
    self.face.set_face_expression(expression)