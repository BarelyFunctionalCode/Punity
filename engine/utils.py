import platform


def invis_tk(root):
  root.overrideredirect(True)
  root.update_idletasks()
  root.wm_attributes("-topmost", True)

  if platform.system() == "Windows":
    root.wm_attributes("-disabled", True)
    root.wm_attributes("-transparentcolor", "white")
    root.config(bg='white')
  else:
    root.wm_attributes("-transparent", True)
    root.config(bg='systemTransparent')

  root.config(cursor='arrow')
  root.geometry("0x0+0+0")

  return root

###################################
############# TkMimic #############
###################################

class TkMimic:
  def __init__(self, x, y, width, height):
    self.x = x
    self.y = y
    self.width = width
    self.height = height

  def winfo_x(self):
    return self.x
  
  def winfo_y(self):
    return self.y
  
  def winfo_width(self):
    return self.width
  
  def winfo_height(self):
    return self.height
  
  def geometry(self, geometry):
    geometry = geometry.split('+')
    self.width, self.height = map(int, geometry[0].split('x'))
    self.x, self.y = map(int, geometry[1:])
  
  def update_idletasks(_):
    pass

  def update(_):
    pass

  def after(self, time, callback):
    pass
    # TODO: Might need to implement this later