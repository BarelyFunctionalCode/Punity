import tkinter as tk
import numpy as np
import types

from engine import Environment

class_blacklist = ['Object', 'Component']


class Inspector:
  def __init__(self, parent):
    self.root_obj = parent.tk_obj
    self.parent = parent

    self.inspector = tk.Toplevel(self.root_obj)
    self.inspector.overrideredirect(True)
    self.inspector.title("punity_inspector")
    self.inspector.geometry(f"300x{Environment.height}+{Environment.width - 300}+0")
    self.inspector.update_idletasks()
    self.inspector.wm_attributes("-alpha", 0.8)
    self.inspector.wm_attributes("-topmost", True)
    self.inspector.update_idletasks()

    self.active_obj = None
    self.obj_info = {}
    self.pane_heights = {}
    self.update_inspector()
  
  def format_value(self, value):
    if isinstance(value, str):
      return value
    elif isinstance(value, bool):
      return 'True' if value else 'False'
    elif isinstance(value, (list, tuple, np.ndarray)):
      return '\n' + ',\n'.join([str(v) for v in value])
    elif isinstance(value, (int, float)):
      return f"{value:.2f}"
    else:
      return value

  def create_label(self, pane, is_title=False, name='', value=''):
    max_name_length = 20
    name_truncated = name[:max_name_length-4] + '...' if len(name) > max_name_length else name
    spacing = ' ' * (max_name_length - len(name_truncated))
    self.obj_info[pane + '_' +name] = tk.Label(
      self.obj_info[pane + '_pane'],
      text=f"{name_truncated}{spacing}{self.format_value(value)}" if not is_title else pane[0].upper() + pane[1:],
      width=50,
      pady=1,
      anchor='w',
      background='#777' if is_title else self.obj_info[pane + '_pane']['background'],
      foreground='black' if is_title else 'white',
      font=('Courier New', 15 if is_title else 9, 'bold' if is_title else 'normal'),
      # wraplength=300,
      # justify=tk.LEFT
    )
    if pane not in self.pane_heights:
      self.pane_heights[pane] = 0
    self.obj_info[pane + '_' +name].place(x=0, y=self.pane_heights[pane], anchor='nw')
    self.inspector.update_idletasks()
    self.pane_heights[pane] += self.obj_info[pane + '_' +name].winfo_height()
    self.obj_info[pane + '_pane'].config(height=self.pane_heights[pane])

  def update_label(self, pane, name, value):
    max_name_length = 20
    name_truncated = name[:max_name_length-4] + '...' if len(name) > max_name_length else name
    spacing = ' ' * (max_name_length - len(name_truncated))
    self.obj_info[pane + '_' + name].config(text=f"{name_truncated}{spacing}{self.format_value(value)}")

  def create_pane(self, name, make_title=False):
    pane_name = name + '_pane'
    self.obj_info[pane_name] = tk.Frame(self.obj_info['master_pane'], width=self.inspector.winfo_width(), background='#333')
    # Get the current height of the master pane
    total_height = sum([self.pane_heights[pane] for pane in self.pane_heights.keys()])
    self.obj_info['master_pane'].create_window(0, total_height, window=self.obj_info[pane_name], anchor=tk.NW)

    if make_title:
      self.create_label(name, True)
    self.inspector.update_idletasks()

  def update_inspector(self):
    if self.active_obj == None:
      self.inspector.after(100, self.update_inspector)
      return
    
    self.update_label('base_object', 'Static', self.active_obj.is_static)
    self.update_label('base_object', 'Collisions', self.active_obj.collision_enabled)
    self.update_label('transform', 'Position', self.active_obj.transform.position)
    self.update_label('transform', 'Direction', self.active_obj.transform.direction)
    self.update_label('transform', 'Size', f"{self.active_obj.transform.width} x {self.active_obj.transform.height}")

    for pane_name in [name[:-5] for name in self.obj_info.keys() if name != 'master_pane' and '_pane' in name]:
      for label_name in [name[len(pane_name)+1:] for name in self.obj_info.keys() if '_pane' not in name and f"{pane_name}_" in name]:
        if hasattr(self.active_obj, label_name):
          self.update_label(pane_name, label_name, getattr(self.active_obj, label_name))
        
    self.inspector.after(100, self.update_inspector)

  def set_active_object(self, obj_name):
    self.active_obj = Environment.get_object(obj_name)

    for label in self.obj_info.values():
      label.destroy()
    self.obj_info = {}
    self.pane_heights = {}

    # Put Object name at the top
    self.obj_info['name'] = tk.Label(self.inspector, text=f"{self.active_obj.name}", width=30, pady=1, anchor='w', font=('Courier New', 20, 'bold'))
    self.obj_info['name'].pack(side=tk.TOP, fill=tk.X)

    # Create a master pane to hold all the other panes
    self.obj_info['master_pane'] = tk.Canvas(
      self.inspector,
      width=self.inspector.winfo_width(),
      height=self.inspector.winfo_height() - self.obj_info['name'].winfo_height(),
      yscrollincrement=5,
    )
    self.obj_info['master_pane'].pack(side=tk.TOP)

    self.inspector.update_idletasks()

    self.create_pane('base_object')
    # Put whether or not the object is static
    self.create_label('base_object', False, 'Static', self.active_obj.is_static)
    # Put whether or not the object has collisions enabled
    self.create_label('base_object', False, 'Collisions', self.active_obj.collision_enabled)

    # Transform information
    self.create_pane('transform', True)
    self.create_label('transform', False, 'Position', self.active_obj.transform.position)
    self.create_label('transform', False, 'Direction', self.active_obj.transform.direction)
    self.create_label('transform', False, 'Size', f"{self.active_obj.transform.width} x {self.active_obj.transform.height}")

    self.create_pane('space')
    self.create_label('space')

    derived_properties=[p for p in dir(self.active_obj) if not isinstance(getattr(self.active_obj,p), types.MethodType) and not p.startswith('__')]
    # Get object base classes
    bases = self.active_obj.__class__.__bases__

    # For each base class not in the blacklist, add a pane and enumerate the properties
    bases_properties = {}
    for base in bases:
      base_name = base.__name__
      class_obj = base()
      base_property_names=[p for p in derived_properties if hasattr(class_obj, p)]
      derived_properties = [p for p in derived_properties if p not in base_property_names]
      class_obj = None
      if base_name not in class_blacklist:
        bases_properties[base_name] = base_property_names

    # Enumerate the properties that the child object defines
    self.create_pane('object')
    for prop in derived_properties:
      self.create_label('object', False, prop, getattr(self.active_obj, prop))

    for base_name, base_property_names in bases_properties.items():
        # Create and title a new pane
        self.create_pane(base_name, True)

        # Enumerate the properties that the base class defines
        for prop in base_property_names:
          self.create_label(base_name, False, prop, getattr(self.active_obj, prop))
    
    self.inspector.update_idletasks()

    # Create srollbar
    total_height = sum([self.pane_heights[pane] for pane in self.pane_heights.keys()])
    self.obj_info['scrollbar'] = tk.Scrollbar(self.inspector)
    self.obj_info['scrollbar'].place(relx=1, rely=0, relheight=1, anchor='ne')
    self.obj_info['master_pane'].config(
      yscrollcommand=self.obj_info['scrollbar'].set,
      scrollregion=(0,0,self.inspector.winfo_width(), total_height)
    )
    self.obj_info['scrollbar'].config(command=self.obj_info['master_pane'].yview)

    def _on_mousewheel(event):
      self.obj_info['master_pane'].yview_scroll(-event.delta, "units")
    def _bind_to_mousewheel(_):
      self.obj_info['master_pane'].bind_all("<MouseWheel>", _on_mousewheel)
    def _unbind_from_mousewheel(_):
      self.obj_info['master_pane'].unbind_all("<MouseWheel>")

    self.obj_info['master_pane'].bind('<Enter>', _bind_to_mousewheel)
    self.obj_info['master_pane'].bind('<Leave>', _unbind_from_mousewheel)