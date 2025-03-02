import time
import math
import threading
import pyautogui
import numpy as np

from display.display import Display

class FACE:
  def __init__(self):
    self.text = ""
    self.expression = ""

    self.display = Display()

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

      # Positioning data
      mouse_position = np.array(pyautogui.position())
      current_display_position = np.array([self.display.root.winfo_x(), self.display.root.winfo_y()])
      new_display_position = np.array([current_display_position[0], current_display_position[1]])
      display_center = np.array([
        current_display_position[0] + self.display.root.winfo_width() // 2,
        current_display_position[1] + self.display.root.winfo_height() // 2
      ])

      # vector between mouse and display center
      distance = np.array([display_center[0] - mouse_position[0], display_center[1] - mouse_position[1]])
      magnitude = np.linalg.norm(distance)
      direction = distance / magnitude

      # Move the display window based on the mouse position
      move_factor = 1.0 - magnitude / self.display_proxity_limit
      move_amount = math.trunc(self.display_move_speed * move_factor)
      new_display_position += (direction * move_amount).astype(np.int32)

      # Update the display window position if needed
      if not np.array_equal(current_display_position, new_display_position):
        self.display.set_window_position(new_display_position)

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