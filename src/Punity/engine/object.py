import time
import numpy as np
from PySide6.QtCore import QRect, QObject

from . import Environment
from .component import Component
from .transform import Transform
from .math import Vector2
from .graphics import QTWindow


class Object(Component, QObject):
  def __init__(self, parent=None, name="root", width=0, height=0, x=0, y=0, is_static=True, **kwargs):
    # Setting the parent and children
    self._is_first_frame = True
    self.parent = parent
    self.children = np.array([])
    self.name = f"{name.lower()}_{id(self)}"
    self.qt_obj = None
    self.graphics = np.array([])

    # Object speficic variables for movement and collision
    self.transform = None
    self.is_static = is_static
    self.collision_enabled = False
    self.collision_ignore_list = []
    self.paused = Environment.paused
    self.last_update_time = time.time()

    # if parent == None and Environment.root != None: return

    self.qt_obj = QTWindow(self) if Environment.root == None else Environment.root.qt_obj

    # Setting the transform component
    parent_position = Vector2([0, 0])
    if parent is not None and parent.transform is not None:
      parent_position = parent.transform.position
    self.transform = Transform(self, x + parent_position.x, y + parent_position.y, width, height)

    self.is_faded = False
    self._is_fading = False
    self.fade_step = 0.05
    self.fade_step_delay = 100
    self._fade_step_timer = 0

    # Init other sibling class instances
    super().__init__(parent=parent if parent is not None else self.qt_obj, objectName=self.name, **kwargs)

    # Adding object to Environment
    Environment.objects = np.append(Environment.objects, self)

    # Adding the object to the parent's children
    if parent != None:
      parent.children = np.append(parent.children, self)

    # Run start function, and start the update loop
    self.start()
    self.update_visuals()

  # Time between the last update and the current update
  @property
  def delta_time(self):
    return (time.time() - self.last_update_time) * 1000
  
  # Update loop for the object
  def _update(self, parent_delta_movement = Vector2([0, 0])):
    if self._is_first_frame: parent_delta_movement = Vector2([0, 0])
    if not self.paused:
      if self.qt_obj == None: return
      # Fading logic
      if self._is_fading and self._fade_step_timer < self.fade_step_delay:
        self._fade_step_timer += self.delta_time
        if self.is_faded:
          done = True
          for graphic in self.graphics:
            if graphic.opacity < 1.0:
              graphic.opacity += self.fade_step
              self._fade_step_timer = 0
              done = False
          if done:
            self.is_faded = False
            self._is_fading = False
        else:
          done = True
          for graphic in self.graphics:
            if graphic.opacity > 0.0:
              graphic.opacity -= self.fade_step
              self._fade_step_timer = 0
              done = False
          if done:
            self.is_faded = True
            self._is_fading = False

      # Run update functionality for derived class and sibling classes
      if parent_delta_movement.magnitude > 0:
        self.transform._position = self.transform._position + parent_delta_movement
      self.update()
      if self.qt_obj == None: return

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

      # Update the position
      delta_movement = self.transform._resolve_position_update()

      # Update the position of the children
      if len(self.children) > 0:
        for child in self.children:
          child._update(parent_delta_movement + delta_movement)

      self.post_update(did_geomentry_update=(parent_delta_movement + delta_movement).magnitude > 0)

    self.last_update_time = time.time()
    if self._is_first_frame: self._is_first_frame = False

  # Functions to be extended by derived/sibling classes
  def start(self):
    super().start()

  def update(self):
    super().update()

  def post_update(self, did_geomentry_update):
      super().post_update(did_geomentry_update)

  def update_visuals(self):
    if self.qt_obj is not None:
      self.qt_obj.update()

  def paint(self, p):
    for graphic in self.graphics:
      graphic.paint(p)

    for child in self.children:
      child.paint(p)

  def set_inputs(self, enabled):
    if self.qt_obj is not None:
      self.qt_obj.set_inputs(enabled)

  def destroy(self):
    if self.parent:
      self.parent.children = np.delete(self.parent.children, np.where(self.parent.children == self))
    Environment.objects = np.delete(Environment.objects, np.where(Environment.objects == self))
    self.update_visuals()

  def _mouse_event(self, event):
    # Iterate children in reverse order to handle top-most first
    for target in reversed(self.children):
      done = target._mouse_event(event)
      if done:
        return True
    else:
      # Starting at the top-most leaf objects, try to process mouse event
      if hasattr(self, "mouse_event") and QRect(*self.transform.rect).contains(event.position().toPoint()):
        self.mouse_event(event)
        return True
    return False

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