import random


class LerpText:
  def __init__(self, text, starting_display_text="", text_transition_time=20.0):
      self._desired_text = text
      self._displayed_text = starting_display_text
      self.text_transition_time = text_transition_time
      self.text_transition_timer = 0.0

  @property
  def text(self):
      return self._displayed_text
  
  @text.setter
  def text(self, value):
      self._desired_text = value
      self.text_transition_timer = 0.0

  def tick(self, delta_time):
      if self.text_transition_timer < self.text_transition_time:
        self.text_transition_timer += delta_time
        return
      self.text_transition_timer = 0.0
  
      length_difference = len(self._desired_text) - len(self._displayed_text)
      if length_difference > 0:
        self._displayed_text += "".join(chr(random.randint(32, 126)) for _ in range(length_difference))
      elif length_difference < 0:
        self._displayed_text = self._displayed_text[:length_difference]
  
      for i in range(len(self._displayed_text)):
        if self._displayed_text[i] != self._desired_text[i]:
          distance_to_target = ord(self._desired_text[i]) - ord(self._displayed_text[i])
          self._displayed_text = self._displayed_text[:i] + \
                                chr(ord(self._displayed_text[i]) + (1 if distance_to_target > 0 else -1)) + \
                                self._displayed_text[i+1:]  