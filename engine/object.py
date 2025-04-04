import tkinter as tk
import time
import numpy as np

from engine import Environment
from engine.component import Component
from engine.transform import Transform
from engine.math import Vector2
from engine.graphics import TkRoot, TkWindow


class Object(Component):
  def __init__(self, parent=None, name="root", width=0, height=0, x=0, y=0, is_static=True, **kwargs):
    # Setting the parent and children
    self._is_first_frame = True
    self.parent = parent
    self.children = np.array([])
    if parent != None:
      parent.children = np.append(parent.children, self)
    self.name = f"{name.lower()}_{id(self)}"
    self.tk_obj = None

    # Object speficic variables for movement and collision
    self.transform = None
    self.is_static = is_static
    self.collision_enabled = False
    self.collision_ignore_list = []
    self.paused = Environment.paused
    self.last_update_time = time.time()

    if parent == None and Environment.root != None: return

    # Setting default TK Window Options
    embed = kwargs.get('embed', False)
    container = kwargs.get('container', False)
    self.tk_obj = TkWindow(parent.tk_obj, embed, container) if parent != None else TkRoot()
    self.tk_obj.title(f"punity_{self.name}")
    self.tk_obj.geometry(f"{width}x{height}+{x}+{y}")
    self.tk_obj.update_idletasks()

    # Setting the transform component
    self.transform = Transform(self)

    self.is_faded = False
    self._is_fading = False
    self.fade_step = 0.05
    self.fade_step_delay = 50
    self._fade_step_timer = 0

    self.images = {}

    # Init other sibling class instances
    super().__init__(**kwargs)

    # Adding object to Environment
    Environment.objects = np.append(Environment.objects, self)

    # Run start function, and start the update loop
    self.start()

  # Time between the last update and the current update
  @property
  def delta_time(self):
    return (time.time() - self.last_update_time) * 1000
  
  # Update loop for the object
  def _update(self, parent_delta_movement = Vector2([0, 0])):
    if self._is_first_frame: parent_delta_movement = Vector2([0, 0])
    if not self.paused:
      if self.tk_obj == None: return
      # Fading logic
      if self._is_fading and self._fade_step_timer < self.fade_step_delay:
        self._fade_step_timer += self.delta_time
        if self.is_faded:
          if self.tk_obj.wm_attributes("-alpha") < 1.0:
            self.tk_obj.wm_attributes("-alpha", self.tk_obj.wm_attributes("-alpha") + self.fade_step)
            self._fade_step_timer = 0
          else:
            self.is_faded = False
            self._is_fading = False
        else:
          if self.tk_obj.wm_attributes("-alpha") > 0.0:
            self.tk_obj.wm_attributes("-alpha", self.tk_obj.wm_attributes("-alpha") - self.fade_step)
            self._fade_step_timer = 0
          else:
            self.is_faded = True
            self._is_fading = False

      # Run update functionality for derived class and sibling classes
      self.transform.position = self.transform.position + parent_delta_movement
      self.transform.did_move_this_frame = False
      old_position = self.transform.position
      self.update()
      if self.tk_obj == None: return

      delta_movement = Vector2([0, 0])

      #TODO: Move collision check to different function that runs after all objects have been updated
      # Check for collisions if the object is not static
      if not self.is_static:
        for obj in Environment.objects:
          if obj == self: continue
          col_normal = self._collision_check(obj)
          if col_normal != None:
            self.on_collision(col_normal, obj)
            # if not obj.is_static:
            #   obj.on_collision(-col_normal, self)

        # Update the position of the TK Window
        if self.transform.did_move_this_frame:
          self.transform.did_move_this_frame = False
          delta_movement = self.transform.position - old_position

      # Update the position of the children
      if len(self.children) > 0:
        for child in self.children:
          child._update(parent_delta_movement + delta_movement)

      new_position = self.transform.position.astype(Vector2.int)
      self.tk_obj.update_idletasks()
      self.tk_obj.geometry(f"{self.transform.width}x{self.transform.height}+{new_position.x}+{new_position.y}")
    self.last_update_time = time.time()
    if self._is_first_frame: self._is_first_frame = False

  # Functions to be extended by derived/sibling classes
  def start(self):
    super().start()

  def update(self):
    super().update()

  # Destroys TK Window and removes object from Environment
  def destroy(self):
    self.tk_obj.destroy()
    self.tk_obj = None
    if self.parent:
      self.parent.children = np.delete(self.parent.children, np.where(self.parent.children == self))
    Environment.objects = np.delete(Environment.objects, np.where(Environment.objects == self))

  # Fade in/out the object
  def fade_in(self):
    if not self.is_faded or self._is_fading: return
    self._is_fading = True

  def fade_out(self):
    if self.is_faded or self._is_fading: return
    self._is_fading = True

  # Debug function to print the hierarchy of the objects in the Environment
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
    col_vec = self.transform.direction

    collision_response = col_normal * col_vec.magnitude
    # print(f"Base Collision: {col_normal} with {other_object.name}; {self.transform.position} {other_object.transform.position}") 
    # print(f"Base Collision: {col_normal} with {other_object.name}; Response: {collision_response} {self.transform.position} {other_object.transform.position}") 
    self.transform.position = self.transform.position + collision_response

    # Apply any addition functionality defined in the derived/sibling class
    super().on_collision(col_normal, col_vec, other_object)