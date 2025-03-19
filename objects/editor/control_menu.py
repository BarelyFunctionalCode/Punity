import tkinter as tk

from environment import Instance as environment

class ControlMenu:
  def __init__(self, parent):
    self.root_obj = parent.tk_obj
    self.parent = parent
    self.controls = tk.Toplevel(self.root_obj)
    self.controls.overrideredirect(True)
    self.controls.title("punity_control_menu")
    self.controls.geometry(f"125x35+{environment.width // 2 - 100}+0")
    self.controls.update_idletasks()
    self.controls.wm_attributes("-alpha", 0.7)
    self.controls.wm_attributes("-topmost", True)
    self.controls.update_idletasks()

    self.pause_button = tk.Button(self.controls, width=3, text="Pause", command=environment.pause, font=('Courier New', 12)).grid(row=0, column=0)
    self.resume_button = tk.Button(self.controls, width=3, text="Resume", command=environment.resume, font=('Courier New', 12)).grid(row=0, column=1)