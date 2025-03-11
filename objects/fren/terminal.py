import tkinter as tk

from utils import invis_tk

class TkinterTerminal:
  def __init__(self, parent_obj, update_queue, talking_queue):
    parent_position = parent_obj.transform.position.astype(int)

    self.tk_obj = invis_tk(tk.Toplevel(parent_obj.tk_obj))
    self.tk_obj.title(f'{parent_obj.tk_obj.title()} Terminal')
    self.tk_obj.geometry(f"300x100+{parent_position[0]}+{parent_position[1] - 100}")
    self.tk_obj.wm_attributes("-alpha", 0.0)

    self.tk_obj.update_idletasks()

    self.update_queue = update_queue
    self.talking_queue = talking_queue
    self.is_active = False
    self.do_destroy = False
    self.is_destroyed = False

    # Terminal Parameters
    self.terminal_text_output = ""
    self.terminal_text_output_index = 0

    # Terminal for text output
    self.frame = tk.Frame(self.tk_obj, bg="black", cursor='none')
    self.frame.pack(fill=tk.BOTH, padx=0, pady=(0,0), side=tk.BOTTOM)

    self.terminal_text = tk.Text(self.frame, state='disabled', wrap='word', bg="black", fg="green", font=("Courier", 10), borderwidth=0, highlightthickness=0, insertbackground="green")
    self.terminal_text.pack(padx=10, pady=10)

    # Add blinking cursor
    self.terminal_text.config(state='normal')
    self.terminal_text.insert(tk.END, "_")
    self.terminal_text.tag_add("cursor", "1.0")
    self.terminal_text.config(state='disabled')

    self.update()
    self.blink_cursor()

  def destroy(self):
    self.do_destroy = True

  def update(self):
    # Fade out terminal
    if self.do_destroy:
      if self.tk_obj.wm_attributes("-alpha") > 0.0:
        self.tk_obj.wm_attributes("-alpha", self.tk_obj.wm_attributes("-alpha") - 0.05)
        self.tk_obj.after(50, self.update)
        return
      self.tk_obj.destroy()
      self.is_destroyed = True
      return

    # Fade in terminal
    if self.tk_obj.wm_attributes("-alpha") < 1.0:
      self.tk_obj.wm_attributes("-alpha", self.tk_obj.wm_attributes("-alpha") + 0.05)
      self.tk_obj.after(50, self.update)
      return
    
    # Update text output from queue
    new_line = False
    if not self.update_queue.empty() and not self.is_active: self.is_active = True
    # if not self.update_queue.empty() and not self.is_active and not self.is_enabled: self.is_active = True
    # if self.is_enabled:
    while not self.update_queue.empty():
      self.terminal_text_output += self.update_queue.get()
    
    if self.terminal_text_output_index < len(self.terminal_text_output):
      self.is_active = True
      
      # Add new character to text object
      char = self.terminal_text_output[self.terminal_text_output_index]
      self.terminal_text.config(state='normal')
      self.terminal_text.insert("end-2c", char)
      self.terminal_text.config(state='disabled')
      if char == "\n" or ((char == "." or char == "?" or char == "!") and char != self.terminal_text_output[min(self.terminal_text_output_index - 1, 0)]):
        new_line = True
      self.terminal_text_output_index += 1
      self.terminal_text.see(tk.END)

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
      self.tk_obj.after(1000, self.update)
    else:
      self.tk_obj.after(50, self.update)

  # Blinking cursor following text output
  def blink_cursor(self):
    if "cursor" in self.terminal_text.tag_names():
      self.terminal_text.config(state='normal')
      self.terminal_text.tag_config(
        "cursor",
        foreground="black" if self.terminal_text.tag_cget("cursor", "foreground") == "green" else "green"
      )
      self.terminal_text.config(state='disabled')
    self.tk_obj.after(500, self.blink_cursor)