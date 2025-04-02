import platform

import tkinter as tk

class TkRoot(tk.Tk):
  def __init__(self):
    super().__init__()
    self.overrideredirect(True)
    self.update_idletasks()
    self.wm_attributes("-topmost", True)

    if platform.system() == "Windows":
      self.wm_attributes("-disabled", True)
      self.wm_attributes("-transparentcolor", "white")
      self.config(bg='white')
    else:
      self.wm_attributes("-transparent", True)
      self.config(bg='systemTransparent')

    self.config(cursor='arrow')
    self.geometry("0x0+0+0")

class TkWindow(tk.Toplevel):
  def __init__(self, parent, embed=False, container=False):
    self.parent = parent
    use = ''
    if embed:
      use = parent.winfo_id()
      self.parent = None
    super().__init__(self.parent, use=use, container=container)
    self.overrideredirect(True)
    self.update_idletasks()
    self.wm_attributes("-topmost", True)

    if platform.system() == "Windows":
      self.wm_attributes("-disabled", True)
      self.wm_attributes("-transparentcolor", "white")
      self.config(bg='white')
    else:
      self.wm_attributes("-transparent", True)
      self.config(bg='systemTransparent')

    self.config(cursor='arrow')
    self.geometry("0x0+0+0")