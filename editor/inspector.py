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
    self.inspector.wm_attributes("-alpha", 0.7)
    self.inspector.wm_attributes("-topmost", True)
    self.inspector.update_idletasks()

    self.active_obj = None

    self.obj_info_lables = {}

  def update_inspector(self, obj_name):
    self.active_obj = environment.get_object(obj_name)

    for label in self.obj_info_lables.values():
      label.destroy()
    self.obj_info_lables = {}

    # Put Object name at the top
    self.obj_info_lables['name'] = tk.Label(self.inspector, text=f"{self.active_obj.name}", width=30, pady=1, anchor='w', font=('Courier New', 20, 'bold'))
    self.obj_info_lables['name'].pack(side=tk.TOP, fill=tk.X)

    # Put whether or not the object is static
    self.obj_info_lables['is_static'] = tk.Label(self.inspector, text=f"Static: {self.active_obj.is_static}", width=30, pady=1, anchor='w', font=('Courier New', 12))
    self.obj_info_lables['is_static'].pack(side=tk.TOP, fill=tk.X)

    # Put whether or not the object has collisions enabled
    self.obj_info_lables['collision_enabled'] = tk.Label(self.inspector, text=f"Collisions: {self.active_obj.collision_enabled}", width=30, pady=1, anchor='w', font=('Courier New', 12))
    self.obj_info_lables['collision_enabled'].pack(side=tk.TOP, fill=tk.X)

    # Create a master pane to hold all the other panes
    self.obj_info_lables['master_pane'] = tk.PanedWindow(self.inspector, orient=tk.VERTICAL)
    self.obj_info_lables['master_pane'].pack(side=tk.TOP, fill=tk.X)

    # Transform information
    self.obj_info_lables['transform_pane'] = tk.PanedWindow(self.inspector, orient=tk.VERTICAL, background='gray')
    self.obj_info_lables['master_pane'].add(self.obj_info_lables['transform_pane'])
    self.obj_info_lables['transform_title'] = tk.Label(self.obj_info_lables['transform_pane'], text=f"Transform", width=30, pady=1, anchor='w', background='darkgray', foreground='black', font=('Courier New', 12))
    self.obj_info_lables['transform_pane'].add(self.obj_info_lables['transform_title'])
    self.obj_info_lables['transform_position'] = tk.Label(self.obj_info_lables['transform_pane'], text=f"Position\t\t{self.active_obj.transform.position}", width=30, pady=1, anchor='w', background=self.obj_info_lables['transform_pane']['background'], font=('Courier New', 12))
    self.obj_info_lables['transform_pane'].add(self.obj_info_lables['transform_position'])
    self.obj_info_lables['transform_last_position'] = tk.Label(self.obj_info_lables['transform_pane'], text=f"Last Position\t{self.active_obj.transform.last_position}", width=30, pady=1, anchor='w', background=self.obj_info_lables['transform_pane']['background'], font=('Courier New', 12))
    self.obj_info_lables['transform_pane'].add(self.obj_info_lables['transform_last_position'])
    self.obj_info_lables['transform_size'] = tk.Label(self.obj_info_lables['transform_pane'], text=f"Size\t\t{self.active_obj.transform.width} x {self.active_obj.transform.height} ", width=30, pady=1, anchor='w', background=self.obj_info_lables['transform_pane']['background'], font=('Courier New', 12))
    self.obj_info_lables['transform_pane'].add(self.obj_info_lables['transform_size'])

    # Child object information
    self.obj_info_lables['object_pane'] = tk.PanedWindow(self.inspector, orient=tk.VERTICAL, background='gray')
    self.obj_info_lables['master_pane'].add(self.obj_info_lables['object_pane'])

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
        class_pane_name = base_name + '_pane'
        self.obj_info_lables[class_pane_name] = tk.PanedWindow(self.inspector, orient=tk.VERTICAL, background='gray')
        self.obj_info_lables['master_pane'].add(self.obj_info_lables[class_pane_name])
        self.obj_info_lables[base_name + '_title'] = tk.Label(self.obj_info_lables[class_pane_name], text=f"{base_name}", width=30, pady=1, anchor='w', background='darkgray', foreground='black', font=('Courier New', 12))
        self.obj_info_lables[class_pane_name].add(self.obj_info_lables[base_name + '_title'])

        # Enumerate the properties that the base class defines
        for prop in base_property_names:
          max_name_length = 20
          prop_truncated = prop[:max_name_length-4] + '...' if len(prop) > max_name_length else prop
          spacing = ' ' * (max_name_length - len(prop_truncated))
          self.obj_info_lables[base_name + '_' + prop] = tk.Label(self.obj_info_lables[class_pane_name], text=f"{prop_truncated}{spacing}{getattr(self.active_obj, prop)}", width=30, pady=1, anchor='w', background=self.obj_info_lables[class_pane_name]['background'], font=('Courier New', 12))
          self.obj_info_lables[class_pane_name].add(self.obj_info_lables[base_name + '_' + prop])
    
    # Enumerate the properties that the child object defines
    for prop in property_names:
      max_name_length = 20
      prop_truncated = prop[:max_name_length-4] + '...' if len(prop) > max_name_length else prop
      spacing = ' ' * (max_name_length - len(prop_truncated))
      self.obj_info_lables[prop] = tk.Label(self.obj_info_lables['object_pane'], text=f"{prop_truncated}{spacing}{getattr(self.active_obj, prop)}", width=30, pady=1, anchor='w', background=self.obj_info_lables['object_pane']['background'], font=('Courier New', 12))
      self.obj_info_lables['object_pane'].add(self.obj_info_lables[prop])