import tkinter as tk
import time
import numpy as np

from components.base import Base
from components.transform import Transform
from utils import Vector2, invis_tk

from environment import Instance as environment

class Object(Base):
  def __init__(self, parent=None, name="root", width=0, height=0, x=0, y=0, is_static=True):
    # Setting the parent and children
    self.parent = parent
    self.children = np.array([])
    if parent != None:
      parent.children = np.append(parent.children, self)

    # Setting default TK Window Options
    self.name = f"{name}_{id(self)}"
    self.tk_obj = invis_tk(tk.Toplevel(parent.tk_obj)) if parent != None else invis_tk(tk.Tk())
    self.tk_obj.title(self.name)
    self.tk_obj.geometry(f"{width}x{height}+{x}+{y}")
    self.tk_obj.update_idletasks()

    # Object speficic variables for movement and collision
    self.is_static = is_static
    self.collision_enabled = False
    self.collision_ignore_list = []
    self.transform = Transform(self)
    self.paused = environment.paused

    # Init other sibling class instances
    super().__init__()

    # Get the list of subclasses of Product
    # subclasses = Object.__subclasses__()

    # # Assuming there is at least one subclass, get the first one
    # if subclasses:
    #     derived_class = subclasses[0]
    #     derived_class_name = derived_class.__name__
    #     print(derived_class_name)  # Output: Book
    # else:
    #     print("No subclasses found")
    # print(self.name)

    # Adding object to environment
    environment.objects = np.append(environment.objects, self)

    # Setting the root object
    if parent == None:
      environment.root = self
      return
    
    # Initialize delta time, run start function, and start the update loop
    self.last_update_time = time.time()
    self.start()
    self._update()

  # Time between the last update and the current update
  @property
  def delta_time(self):
    return (time.time() - self.last_update_time) * 1000
  
  # Update loop for the object
  def _update(self):
    if not self.paused:
      # Run update functionality for derived class and sibling classes
      if self.tk_obj == None: return
      self.update()
      if self.tk_obj == None: return

      # Check for collisions if the object is not static
      if not self.is_static:
        for obj in environment.objects:
          if obj == self: continue
          col_normal = self._collision_check(obj)
          if col_normal != None:
            self.on_collision(col_normal, obj)
            if not obj.is_static:
              obj.on_collision(-col_normal, self)

        # Update the position of the TK Window
        new_position = self.transform.position.astype(Vector2.int)
        self.tk_obj.update_idletasks()
        self.tk_obj.geometry(f"{self.transform.width}x{self.transform.height}+{new_position.x}+{new_position.y}")
    # Update delta time
    self.last_update_time = time.time()
    self.tk_obj.after(10, self._update)

  # Functions to be extended by derived/sibling classes
  def start(self):
    super().start()

  def update(self):
    super().update()

  # Destroys TK Window and removes object from environment
  def destroy(self):
    self.tk_obj.destroy()
    self.tk_obj = None
    if self.parent:
      self.parent.children = np.delete(self.parent.children, np.where(self.parent.children == self))
    environment.objects = np.delete(environment.objects, np.where(environment.objects == self))

  # Begins the main loop for the root object
  def begin(self):
    if self.parent: return
    try:
      self.tk_obj.mainloop()
    except:
      self.destroy()

  # Debug function to print the hierarchy of the objects in the environment
  def print_hierarchy(self, depth=0):
    print(f"{' ' * depth}|{self.name}")
    for child in self.children:
      child.print_hierarchy(depth + 1)

  def generate_hierarchy(self, depth=0):
    hierarchy = {}
    hierarchy[self.name] = {}
    for child in self.children:
      hierarchy[self.name].update(child.generate_hierarchy(depth + 1))
    return hierarchy
  
  # Debug function to toggle the outline of the object
  def toggle_outline(self):
    Exception("Not Implemented")
  
  # Collision Detection
  def _collision_check(self, other):
    # Check if either object has collision enabled and if they are in each other's ignore list
    if not self.collision_enabled or not other.collision_enabled: return None
    if other.name in self.collision_ignore_list: return None
    if self.name in other.collision_ignore_list: return None

    # Check if the objects are colliding
    did_collide = False
    if self.transform.position.x < other.transform.position.x + other.transform.width and \
       self.transform.position.x + self.transform.width > other.transform.position.x and \
       self.transform.position.y < other.transform.position.y + other.transform.height and \
       self.transform.position.y + self.transform.height > other.transform.position.y:
      did_collide = True
    
    if did_collide:
      # Get Collision vector
      collision_relative_position = self.transform.position - other.transform.position

      possible_collisions = np.array([
        # Top side
        collision_relative_position.y + self.transform.height,
        # Left side
        collision_relative_position.x + self.transform.width,
        # Bottom side
        collision_relative_position.y - other.transform.height,
        # Right side
        collision_relative_position.x - other.transform.width,
      ])

      directions = np.array([
        Vector2.up,
        Vector2.left,
        Vector2.down,
        Vector2.right,
      ])

      # Get the normal of the collision
      return directions[np.argmin(np.abs(possible_collisions))]
    return None

  # Collision Response
  def on_collision(self, col_normal, other_object):
    # Get the collision vector and apply a response to the collision to keep the objects from overlapping
    col_vec = self.transform.position - self.transform.last_position

    collision_response = col_normal * col_vec.magnitude
    # print(f"Base Collision: {col_normal} with {other_object.name}; {self.transform.position} {other_object.transform.position}") 
    # print(f"Base Collision: {col_normal} with {other_object.name}; Response: {collision_response} {self.transform.position} {other_object.transform.position}") 
    self.transform.position = self.transform.position + collision_response

    # Apply any addition functionality defined in the derived/sibling class
    super().on_collision(col_normal, col_vec, other_object)