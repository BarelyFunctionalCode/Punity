import time
import threading

from Punity import Scene
from Punity.engine.event import Event

from Punity.assets.objects.frame import Frame

class Brain:
  def __init__(self):
    self.on_response_event = Event()
    self.input = None

  def loop(self):
    while True:
      if self.input is not None:
        time.sleep(5.0)
        self.on_response_event.invoke(f"You're a <!red!>moron")
        self.input = None
      time.sleep(0.01)

  def on_submit(self, text):
    self.input = text

  def add_response_listener(self, listener):
    self.on_response_event.add_listener(listener)

  def remove_response_listener(self, listener):
    self.on_response_event.remove_listener(listener)


if __name__ == "__main__":

  # Root object for all other objects to spawn from
  scene = Scene(False)

  # Stand-in for the real dummy
  brain = Brain()

  # Create the frame object and link it with the brain
  frame = Frame(scene)
  frame.add_submit_listener(brain.on_submit)
  brain.add_response_listener(frame.on_response)

  # Start the brain's loop in a separate thread
  threading.Thread(target=brain.loop, daemon=True).start()

  # Run the main loop
  scene.begin()