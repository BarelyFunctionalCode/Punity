import time
import threading

from display.display import Display
from display.environment import Instance as environment
from display.object.object import Object
from display.utils import TkMimic

class FACE:
  def __init__(self):
    self.text = ""
    self.expression = ""

    self.bounds = environment.bounds
    self.bounds_thickness = environment.bounds_thickness

    # Top
    Object('top_bound', TkMimic(self.bounds[3], self.bounds[0] - self.bounds_thickness, self.bounds[1] - self.bounds[3], self.bounds_thickness))
    # Right
    Object('right_bound', TkMimic(self.bounds[1], self.bounds[0], self.bounds_thickness, self.bounds[2] - self.bounds[0]))
    # Bottom
    Object('bottom_bound', TkMimic(self.bounds[3], self.bounds[2], self.bounds[1] - self.bounds[3], self.bounds_thickness))
    # Left
    Object('left_bound', TkMimic(self.bounds[3] - self.bounds_thickness, self.bounds[0], self.bounds_thickness, self.bounds[2] - self.bounds[0]))

    self.display = Display('fren')

    self.display_proxity_limit = 300
    self.display_move_speed = 100

    self.new_thread = threading.Thread(target=self.worker)
    self.new_thread.start()

  def worker(self):
    while True:
      # If the display window is closed, break the loop
      if self.display.root == None: break

      # Update the display window with the new text and expression
      if self.text != "":
        self.display.enqueue_update_text(self.text + "\n\n")
        self.text = ""
      if self.expression != "":
        self.display.set_face_expression(self.expression)
        self.expression = ""

      time.sleep(0.1)

  def start(self):
    self.display.start()
    self.new_thread.join()

  def speak(self, text):
    self.text = text

  def update_expression(self, expression):
    self.expression = expression


if __name__ == "__main__":
  face = FACE()
  
  # face.speak("Death to all humans")
  face.update_expression("slow_scan")

  face.start()