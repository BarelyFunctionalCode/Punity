import time
import threading
import tkinter as tk

from environment import Instance as environment

from objects.display import Display
from objects.border import Border

from utils import invis_tk

class Fren:
  def __init__(self):
    self.text = ""
    self.expression = ""

    Border(environment.x, environment.y, environment.width, environment.height, 50)

    self.root = invis_tk(tk.Tk())
    self.display = Display('fren', self.root)

    self.new_thread = threading.Thread(target=self.worker)
    self.new_thread.start()

  def worker(self):
    while True:
      # If the display window is closed, break the loop
      if self.root == None: break

      # Update the display window with the new text and expression
      if self.text != "":
        self.display.enqueue_update_text(self.text + "\n\n")
        self.text = ""
      if self.expression != "":
        self.display.set_face_expression(self.expression)
        self.expression = ""

      time.sleep(0.1)

  def start(self):
    try:
      self.root.mainloop()
    except:
      self.root.destroy()
      self.root = None
    self.new_thread.join()

  def speak(self, text):
    self.text = text

  def update_expression(self, expression):
    self.expression = expression


if __name__ == "__main__":
  fren = Fren()
  
  # face.speak("Death to all humans")
  fren.update_expression("slow_scan")

  fren.start()