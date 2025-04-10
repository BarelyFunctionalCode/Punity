from queue import Queue

from engine import Object, Environment
from engine.math import Vector2

from assets.components.rigidbody import Rigidbody
from assets.objects.terminal import Terminal


from .movement import Movement
from .face import Face
from . import actions


class Fren(Object, Face, Movement, Rigidbody):
  def __init__(self, parent, entrance=None):
    # Setting up the entrance that's defined
    self.face_polygon = [20,0, 120,0, 140,20, 145,90, 120,140, 90,160, 50,160, 20,140, -5,90, 0,20, 20,0,]
    x = 200
    y = 200
    self.entrance = None
    if entrance in actions.entrances:
      self.entrance = actions.entrances[entrance]
      x = self.entrance.spawn_position.x
      y = self.entrance.spawn_position.y

    self.is_busy = False
    self.inactivity_timer = 0
    self.inactivity_timeout = 2000
    self.asleep_timer = 0
    self.asleep_fade_timeout = 20000
    self.terminal_despawn_timer = 0
    self.terminal_despawn_timeout = 5000
    self.terminal = None
    self.terminal_update_queue = Queue()
    super().__init__(parent, 'fren', 140, 170, x, y, False)
    
  def start(self):
    super().start()
    # Initializing gravity as disabled
    self.use_gravity = False

    # Run the entrance
    if self.entrance:
      self.entrance = self.entrance(self.parent, self)

    Environment.new_application_event.add_listener(self.new_application_trigger)
    Environment.new_input_event.add_listener(self.new_input_event_trigger)
    # self.tk_obj.after(12000, lambda: self.enqueue_update_text("I make big shid, and I'm not sorry.\n\n\n💩"))

  def update(self):
    super().update()
    self.is_busy = (self.terminal and self.terminal.is_active) or self.is_face_active
    if self.is_busy:
      self.inactivity_timer = 0
      return
    

    if self.inactivity_timer < self.inactivity_timeout:
      self.inactivity_timer += self.delta_time
    else:
      self.set_face_expression("sleep")

      # Once asleep for long enough, fade out
      if self.asleep_timer < self.asleep_fade_timeout:
        self.asleep_timer += self.delta_time
      else:
        self.fade_out()


    # TODO: Terminal should destroy itself when it's done
    if self.terminal and self.terminal.is_destroyed:
      self.terminal = None

    if not self.terminal and not self.terminal_update_queue.empty():
      terminal_position = self.transform.position.astype(int) - Vector2([0, 100])
      self.terminal = Terminal(self, terminal_position.x, terminal_position.y, 5000, self.terminal_update_queue, self.talking_queue)

    if self.is_face_asleep and self.move_mode != 'sleep':
      self.set_move_mode('sleep')

  def wake_up(self):
    if not self.is_face_asleep:
      return
    self.asleep_timer = 0
    self.fade_in()
    self.set_face_expression("wake")

  # Used by the assistant to update the terminal text
  def enqueue_update_text(self, text):
    self.wake_up()
    self.terminal_update_queue.put(text)

  # Behavior triggers
  
  def new_application_trigger(self, app_pid):
    self.enqueue_update_text(f"New application detected: {app_pid}")

  def new_input_event_trigger(self, event_data):
    print(event_data)