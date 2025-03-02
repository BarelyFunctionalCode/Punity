import tkinter as tk
import math
import numpy as np

from .face import TkinterFace
from .terminal import TkinterTerminal

def away_from_zero(x):
  return int(x // 1 + 2 ** (x > 0) - 1)

class Display:
  def __init__(self):
    # Initialize base Tkinter window and the face and terminal objects
    self.root = tk.Tk()
    self.root.title("Face")
    self.root.geometry("200x200+100+100")
    self.root.config(cursor='none', bg='gray')

    self.root.overrideredirect(True)
    self.root.lift()
    self.root.wm_attributes("-topmost", True)
    self.root.wm_attributes("-disabled", True)
    # self.root.wm_attributes("-transparentcolor", "black")

    self.is_active = True
    self.is_waking_up = False
    self.inactivity_timer = 0
    self.inactivity_timeout = 500

    self.desired_window_position = np.array([300, 300])
    self.window_move_step = 0.1

    self.face = TkinterFace(self.root)
    # self.terminal = TkinterTerminal(self.root, self.face.talking_queue)
    self.update_window_position()

  def stop(self):
    # Stop the Tkinter main loop
    self.root.destroy()
    self.root = None

  def start(self):
    # Start the Tkinter main loop
    self.check_activity()
    self.root.bind_all("<Control-c>", lambda e: self.stop())
    self.root.mainloop()
    
  def check_activity(self):
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

    self.root.after(10, self.check_activity)

  # Used by the assistant to update the face parameters
  def enqueue_update_face(self, new_face_parameters, duration):
    self.face.update_queue.put((new_face_parameters, duration))

  # Used by the assistant to update the terminal text
  def enqueue_update_text(self, text):
    self.terminal.update_queue.put(text)

  # Used by the assistant to set the face expression
  def set_face_expression(self, expression):
    self.face.set_face_expression(expression)

  def update_window_position(self):
    # Update the window position and size
    current_position = (self.root.winfo_x(), self.root.winfo_y())
    new_position = np.array([
      current_position[0] + away_from_zero((self.desired_window_position[0] - current_position[0]) * self.window_move_step),
      current_position[1] + away_from_zero((self.desired_window_position[1] - current_position[1]) * self.window_move_step)
    ])

    if abs(new_position[0] - self.desired_window_position[0]) <= 1:
      new_position = np.array([self.desired_window_position[0], new_position[1]])
    if abs(new_position[1] - self.desired_window_position[1]) <= 1:
      new_position = np.array([new_position[0], self.desired_window_position[1]])

    self.root.update_idletasks()
    # print(f"{self.root.winfo_width()}x{self.root.winfo_height()}+{new_position[0]}+{new_position[1]}")
    self.root.geometry(f"{self.root.winfo_width()}x{self.root.winfo_height()}+{new_position[0]}+{new_position[1]}")

    # print(f"Current Position: {current_position} | New Position: {new_position} | Desired Position: {self.desired_window_position}")

    if not np.array_equal(current_position, new_position):
      self.root.after(10, self.update_window_position)

  def set_window_position(self, position):
    # print(f"Setting window position to {position}")
    self.desired_window_position = position
    self.update_window_position()