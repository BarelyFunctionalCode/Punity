import tkinter as tk

from objects.object import Object

class Terminal(Object):
  def __init__(self, parent, x, y, update_queue, talking_queue):
    self.update_queue = update_queue
    self.talking_queue = talking_queue

    super().__init__(parent, 'terminal', 300, 100, x, y, True)

  def start(self):
    super().start()
    self.update_delay = 50
    self.update_delay_timer = 0
    self.is_active = False
    self.do_destroy = False
    self.is_destroyed = False

    # Terminal Parameters
    self.terminal_text_output = ""
    self.terminal_text_output_index = 0

    # Terminal for text output
    self.frame = tk.Frame(self.tk_obj, bg="black", cursor='none')
    self.frame.pack(fill=tk.BOTH, padx=0, pady=(0,0), side=tk.BOTTOM, expand=True)
    self.terminal_text = tk.Message(self.frame, bg="black", fg="green", font=("Courier New", 12), borderwidth=0, highlightthickness=0, justify=tk.LEFT, width=280, anchor=tk.NW)
    self.terminal_text.pack(side=tk.TOP, padx=10, pady=10, fill=tk.BOTH, expand=True)

    self.terminal_text.config(text="_")

    self.update()
    self.blink_cursor()

  def start_destroy(self):
    self.do_destroy = True

  def update(self):
    super().update()

    self.update_delay_timer += self.delta_time
    if self.update_delay_timer < self.update_delay:
      return
    self.update_delay_timer = 0

    # Fade out terminal
    if self.do_destroy:
      if self.tk_obj.wm_attributes("-alpha") > 0.0:
        self.tk_obj.wm_attributes("-alpha", self.tk_obj.wm_attributes("-alpha") - 0.05)
        self.update_delay = 50
        return
      self.destroy()
      self.is_destroyed = True
      return

    # Fade in terminal
    if self.tk_obj.wm_attributes("-alpha") < 1.0:
      self.tk_obj.wm_attributes("-alpha", self.tk_obj.wm_attributes("-alpha") + 0.05)
      self.update_delay = 50
      return
    
    # Update text output from queue
    new_line = False
    if not self.update_queue.empty() and not self.is_active: self.is_active = True
    while not self.update_queue.empty():
      self.terminal_text_output += self.update_queue.get()
    
    if self.terminal_text_output_index < len(self.terminal_text_output):
      self.is_active = True
      
      # Add new character to text object
      char = self.terminal_text_output[self.terminal_text_output_index]
      current_cursor = self.terminal_text.cget('text')[-1]
      self.terminal_text.config(text=self.terminal_text_output[:self.terminal_text_output_index+1] + current_cursor)
      if char == "\n" or ((char == "." or char == "?" or char == "!") and char != self.terminal_text_output[min(self.terminal_text_output_index - 1, 0)]):
        new_line = True
      self.terminal_text_output_index += 1

      # TODO: Make a terminal variant that has this code
      # Update talking queue to move the mouth when text is outputting
      if char == " " or new_line:
        self.talking_queue.put(0.0)
      else:
        self.talking_queue.put(0.7)
    else:
      self.is_active = False
      self.talking_queue.put(0.0)
  
    # Longer delay after new line
    if new_line:
      self.update_delay = 1000
    else:
      self.update_delay = 50

  # Blinking cursor following text output
  def blink_cursor(self):
    current_output = self.terminal_text.cget('text')
    current_output = current_output[:-1] + (" " if current_output[-1] == "_" else "_")
    self.terminal_text.config(text=current_output)
    self.tk_obj.after(500, self.blink_cursor)