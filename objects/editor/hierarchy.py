import tkinter as tk

from environment import Instance as environment

class Hierarchy:
  def __init__(self, parent, inspector, force_expand=False):
    self.root_obj = parent.tk_obj
    self.parent = parent
    self.inspector = inspector
    self.force_expand = force_expand

    self.hierarchy = tk.Toplevel(self.root_obj)
    self.hierarchy.overrideredirect(True)
    self.hierarchy.title("Hierarchy")
    self.hierarchy.geometry(f"200x{environment.height}+0+0")
    self.hierarchy.update_idletasks()
    self.hierarchy.wm_attributes("-alpha", 0.8)
    self.hierarchy.wm_attributes("-topmost", True)
    self.hierarchy.update_idletasks()

    self.hierarchy_objs = {}
    self.update_hierarchy()

  
  def update_hierarchy(self):
    hierarchy_dict = self.parent.generate_hierarchy()
    self.i = 0
    self.delete_hierarchy_objs(list(hierarchy_dict.values())[0])
    self.update_hierarchy_objs(list(hierarchy_dict.values())[0])
    self.hierarchy.after(100, self.update_hierarchy)

  def delete_hierarchy_objs(self, dict, start=True, hierarchy_keys=[]):
    if len(hierarchy_keys) == 0:
      hierarchy_keys = list(self.hierarchy_objs.keys())
    for obj_name, children in dict.items():
      obj_name = obj_name.lower()
      if obj_name in hierarchy_keys:
        hierarchy_keys.remove(obj_name)

      if len(children) > 0:
        self.delete_hierarchy_objs(children, False, hierarchy_keys)

    if start:
      for obj_name in hierarchy_keys:
        self.hierarchy_objs[obj_name]['toggle'].destroy()
        self.hierarchy_objs[obj_name]['obj'].destroy()
        self.hierarchy_objs.pop(obj_name)

  def update_hierarchy_objs(self, dict, depth=0):
    for obj_name, children in dict.items(): ## SOMETHING IS WRONG HERE
      obj_name = obj_name.lower()
      if obj_name not in self.hierarchy_objs.keys():
        new_toggle = tk.Label(self.hierarchy, name=obj_name+'_toggle', text='-' if self.force_expand else '+' , width=1, pady=1, anchor='w', font=('Courier New', 12))
        new_toggle.place(x=5+depth*30, y=self.i*25)
        new_toggle.bind("<Button-1>", self.on_hierarchy_obj_toggle)

        new_obj = tk.Label(self.hierarchy, name=obj_name, text='_'.join(obj_name.split('_')[:-1]), width=20, pady=1, anchor='w', justify=tk.LEFT, font=('Courier New', 12))
        new_obj.place(x=20+depth*30, y=self.i*25)
        new_obj.bind("<Button-1>", self.set_active_obj)

        self.hierarchy_objs[obj_name] = {'toggle': new_toggle, 'obj': new_obj, 'expanded': self.force_expand}
      else:
        self.hierarchy_objs[obj_name]['toggle'].place(x=5+depth*30, y=self.i*25)
        self.hierarchy_objs[obj_name]['obj'].place(x=20+depth*30, y=self.i*25)

      self.i += 1
      is_expanded = self.hierarchy_objs[obj_name]['expanded']
      if is_expanded:
        self.update_hierarchy_objs(children, depth + 1)

      self.hierarchy.update_idletasks()

  def on_hierarchy_obj_toggle(self, event):
    if event.widget.winfo_class() == 'Label':
      toggled_obj_name = '_'.join(event.widget.winfo_name().split('_')[:-1])
      self.hierarchy_objs[toggled_obj_name]['expanded'] = not self.hierarchy_objs[toggled_obj_name]['expanded']
      if self.hierarchy_objs[toggled_obj_name]['expanded']:
        self.hierarchy_objs[toggled_obj_name]['toggle'].config(text='-')
      else:
        self.hierarchy_objs[toggled_obj_name]['toggle'].destroy()
        self.hierarchy_objs[toggled_obj_name]['obj'].destroy()
        self.hierarchy_objs.pop(toggled_obj_name)

        current_obj = [environment.objects[i] for i in range(len(environment.objects)) if environment.objects[i].name.lower() == toggled_obj_name][0]
        def destroy_children(obj):
          if len(obj.children) > 0:
            for child in obj.children:
              if child.name.lower() in self.hierarchy_objs.keys():
                self.hierarchy_objs[child.name.lower()]['toggle'].destroy()
                self.hierarchy_objs[child.name.lower()]['obj'].destroy()
                self.hierarchy_objs.pop(child.name.lower())
                destroy_children(child)
        destroy_children(current_obj)

  def set_active_obj(self, event):
    if event.widget.winfo_class() == 'Label':
      if self.inspector:
        self.inspector.set_active_object(event.widget.winfo_name())
      for obj_name in self.hierarchy_objs.keys():
        if obj_name == event.widget.winfo_name():
          self.hierarchy_objs[obj_name]['obj'].config(bg='lightblue', foreground='black')
          self.hierarchy_objs[obj_name]['toggle'].config(bg='lightblue', foreground='black')
        else:
          self.hierarchy_objs[obj_name]['obj'].config(bg=self.root_obj['bg'], foreground='white')
          self.hierarchy_objs[obj_name]['toggle'].config(bg=self.root_obj['bg'], foreground='white')
    self.hierarchy.update_idletasks()