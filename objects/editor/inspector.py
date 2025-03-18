import tkinter as tk
import types

from environment import Instance as environment

class_blacklist = ['Object', 'Base']

class Inspector:
  def __init__(self, parent):
    self.root_obj = parent.tk_obj
    self.parent = parent

    self.inspector = tk.Toplevel(self.root_obj)
    self.inspector.overrideredirect(True)
    self.inspector.title("Hierarchy")
    self.inspector.geometry(f"300x{environment.height}+{environment.width - 300}+0")
    self.inspector.update_idletasks()
    self.inspector.wm_attributes("-alpha", 0.8)
    self.inspector.wm_attributes("-topmost", True)
    self.inspector.update_idletasks()

    self.active_obj = None

    self.obj_info = {}

    self.update_inspector()
  
  def create_label(self, pane, is_title=False, name='', value=''):
    max_name_length = 20
    name_truncated = name[:max_name_length-4] + '...' if len(name) > max_name_length else name
    spacing = ' ' * (max_name_length - len(name_truncated))
    self.obj_info[pane + '_' +name] = tk.Label(
      self.obj_info[pane + '_pane'],
      text=f"{name_truncated}{spacing}{value}" if not is_title else pane[0].upper() + pane[1:],
      width=30,
      pady=1,
      anchor='w',
      background='#777' if is_title else self.obj_info[pane + '_pane']['background'],
      foreground='black' if is_title else 'white',
      font=('Courier New', 15 if is_title else 12, 'bold' if is_title else 'normal'),
      # wraplength=300,
      # justify=tk.LEFT
    )
    self.obj_info[pane + '_pane'].add(self.obj_info[pane + '_' +name])

  def update_label(self, pane, name, value):
    max_name_length = 20
    name_truncated = name[:max_name_length-4] + '...' if len(name) > max_name_length else name
    spacing = ' ' * (max_name_length - len(name_truncated))
    self.obj_info[pane + '_' + name].config(text=f"{name_truncated}{spacing}{value}")

  def create_pane(self, name, make_title=False):
    pane_name = name + '_pane'
    self.obj_info[pane_name] = tk.PanedWindow(self.inspector, orient=tk.VERTICAL, background='#333')
    self.obj_info['master_pane'].add(self.obj_info[pane_name])

    if make_title:
      self.create_label(name, True)

  def update_inspector(self):
    if self.active_obj == None:
      self.inspector.after(100, self.update_inspector)
      return
    
    self.update_label('base_object', 'Static', self.active_obj.is_static)
    self.update_label('base_object', 'Collisions', self.active_obj.collision_enabled)
    self.update_label('transform', 'Position', self.active_obj.transform.position)
    self.update_label('transform', 'Last Position', self.active_obj.transform.last_position)
    self.update_label('transform', 'Size', f"{self.active_obj.transform.width} x {self.active_obj.transform.height}")

    for pane_name in [name[:-5] for name in self.obj_info.keys() if name != 'master_pane' and '_pane' in name]:
      for label_name in [name[len(pane_name)+1:] for name in self.obj_info.keys() if '_pane' not in name and f"{pane_name}_" in name]:
        if hasattr(self.active_obj, label_name):
          self.update_label(pane_name, label_name, getattr(self.active_obj, label_name))
        
    self.inspector.after(100, self.update_inspector)

  def set_active_object(self, obj_name):
    self.active_obj = environment.get_object(obj_name)

    for label in self.obj_info.values():
      label.destroy()
    self.obj_info = {}

    # Put Object name at the top
    self.obj_info['name'] = tk.Label(self.inspector, text=f"{self.active_obj.name}", width=30, pady=1, anchor='w', font=('Courier New', 20, 'bold'))
    self.obj_info['name'].pack(side=tk.TOP, fill=tk.X)

    # Create a master pane to hold all the other panes
    self.obj_info['master_pane'] = tk.PanedWindow(self.inspector, orient=tk.VERTICAL)
    self.obj_info['master_pane'].pack(side=tk.TOP, fill=tk.X)

    self.create_pane('base_object')
    # Put whether or not the object is static
    self.create_label('base_object', False, 'Static', self.active_obj.is_static)
    # Put whether or not the object has collisions enabled
    self.create_label('base_object', False, 'Collisions', self.active_obj.collision_enabled)

    # Transform information
    self.create_pane('transform', True)
    self.create_label('transform', False, 'Position', self.active_obj.transform.position)
    self.create_label('transform', False, 'Last Position', self.active_obj.transform.last_position)
    self.create_label('transform', False, 'Size', f"{self.active_obj.transform.width} x {self.active_obj.transform.height}")

    self.create_pane('space')
    self.create_label('space')

    # Child object information
    self.create_pane('object')

    property_names=[p for p in dir(self.active_obj) if not isinstance(getattr(self.active_obj,p), types.MethodType) and not p.startswith('__')]
    # Get object base classes
    bases = self.active_obj.__class__.__bases__

    # For each base class not in the blacklist, add a pane and enumerate the properties
    for base in bases:
      base_name = base.__name__
      class_obj = base()
      base_property_names=[p for p in property_names if hasattr(class_obj, p)]
      property_names = [p for p in property_names if p not in base_property_names]
      class_obj = None
      if base_name not in class_blacklist:
        # Create and title a new pane
        self.create_pane(base_name, True)

        # Enumerate the properties that the base class defines
        for prop in base_property_names:
          self.create_label(base_name, False, prop, getattr(self.active_obj, prop))
    
    # Enumerate the properties that the child object defines
    for prop in property_names:
      self.create_label('object', False, prop, getattr(self.active_obj, prop))