import tkinter as tk

from environment import Instance as environment

class ControlMenu:
  def __init__(self, parent):
    self.parent = parent
    self.tk_obj = tk.Toplevel(parent)
    self.tk_obj.overrideredirect(True)
    self.tk_obj.title("Control Menu")
    self.tk_obj.geometry(f"125x35+{environment.width // 2 - 100}+0")
    self.tk_obj.update_idletasks()
    self.tk_obj.wm_attributes("-alpha", 0.7)
    self.tk_obj.wm_attributes("-topmost", True)
    self.tk_obj.update_idletasks()

    self.pause_button = tk.Button(self.tk_obj, width=3, text="Pause", command=environment.pause).grid(row=0, column=0)
    self.resume_button = tk.Button(self.tk_obj, width=3, text="Resume", command=environment.resume).grid(row=0, column=1)