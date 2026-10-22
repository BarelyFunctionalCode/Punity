import tkinter as tk

from engine import Environment

class ControlMenu:
  def __init__(self, editor, parent):
    self.editor = editor
    self.root_obj = parent.tk_obj
    self.parent = parent
    self.controls = tk.Toplevel(self.root_obj)
    self.controls.overrideredirect(True)
    self.controls.title("punity_control_menu")
    self.controls.geometry(f"270x35+{Environment.width // 2 - 135}+0")
    self.controls.update_idletasks()
    self.controls.wm_attributes("-alpha", 0.7)
    self.controls.wm_attributes("-topmost", True)
    self.controls.update_idletasks()

    self.create_inspector = editor.create_inspector
    self.destroy_inspector = editor.destroy_inspector
    self.create_hierarchy = editor.create_hierarchy
    self.destroy_hierarchy = editor.destroy_hierarchy

    self.hierarchy_button = tk.Button(self.controls, width=5, text="Hierarchy", command=lambda:self.toggle_hierarchy(), font=('Courier New', 12))
    self.pause_button = tk.Button(self.controls, width=3, text="Pause", command=Environment.pause, font=('Courier New', 12))
    self.resume_button = tk.Button(self.controls, width=3, text="Resume", command=Environment.resume, font=('Courier New', 12))
    self.inspector_button = tk.Button(self.controls, width=5, text="Inspector", command=lambda:self.toggle_inspector(), font=('Courier New', 12))
    
    self.hierarchy_button.grid(row=0, column=0)
    self.pause_button.grid(row=0, column=1)
    self.resume_button.grid(row=0, column=2)
    self.inspector_button.grid(row=0, column=3)

  def toggle_inspector(self):
    if self.editor.inspector is None:
      self.create_inspector()
      self.inspector_button.config(text="X")
    else:
      self.destroy_inspector()
      self.inspector_button.config(text="Inspector")

  def toggle_hierarchy(self):
    if self.editor.hierarchy is None:
      self.create_hierarchy()
      self.hierarchy_button.config(text="X")
    else:
      self.destroy_hierarchy()
      self.hierarchy_button.config(text="Hierarchy")