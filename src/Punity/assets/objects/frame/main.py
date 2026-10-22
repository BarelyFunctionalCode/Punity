import time
from PySide6.QtGui import QColor

from Punity.engine import Object
from Punity.engine.event import Event
from Punity.engine.environment import Environment
from Punity.engine.graphics import Text, Rectangle
from Punity.engine.math.vector2 import Vector2

from Punity.assets.objects.basics.button import Button
from Punity.assets.objects.basics.lerpText import LerpText
from Punity.assets.objects.basics.inputBox import InputBox
from Punity.assets.objects.basics.outputBox import OutputBox


"""
#845ec2
#d65db1
#ff6f91
#ff9671
#ffc75f
#f9f871
"""

class Frame(Object):
  def __init__(self, parent):
    self.on_submit_event = Event()

    self.container = None
    self.content = None
    self.input_box = None
    self.output_box = None
    self.button = None

    self.current_state = "closed"
    self.previous_state = "closed"
    self.states = {
      "open": {
        "x": Environment.width // 2,
        "y": Environment.height // 2,
        "container_color": "#845ec2",
        "container_opacity": 0.8,
        "container_rect": [-250, -75, 500, 150],
        "container_hole_rect": [10, 40, 400, 100],
        "content_rect": [-240, -35, 400, 100],
        "content_opacity": 0.5,
        "text_rect": [-240, -75, 400, 40],
        "text_size": 18,
        "text_opacity": 1.0,
        "text_color": "white",
        "button_rect": [170, -65, 60, 130],
      },
      "closed": {
        "x": 10,
        "y": 10,
        "container_color": "#f9f871",
        "container_opacity": 0.3,
        "container_rect": [-25, -25, 50, 50],
        "container_hole_rect": [-10, 0, 0, 0],
        "content_rect": [0, 10, 0, 0],
        "content_opacity": 0.0,
        "text_rect": [0, -10, 0, 0],
        "text_opacity": -1.0,
        "text_size": 0,
        "text_color": "white",
        "button_rect": [10, 0, 0, 0],
      },
      "submitted": {
        "x": 100,
        "y": 100,
        "container_color": "#d65db1",
        "container_opacity": 0.8,
        "container_rect": [0, 0, 600, 300],
        "container_hole_rect": [-10, 0, 0, 0],
        "content_rect": [0, 10, 0, 0],
        "content_opacity": 0.0,
        "text_rect": [10, 10, 580, 280],
        "text_opacity": 1.0,
        "text_color": "white",
        "text_size": 14,
        "button_rect": [300, 40, 0, 0],
      }
    }

    self.state_transition_time = 500.0
    self.state_transition_timer = 0.0
    self.is_transitioning = False
    self.last_activation_time = time.time()


    self.lerp_text_handler = LerpText("What the fuck do you want.")


    super().__init__(parent, "frame", 0, 0, self.states[self.current_state]["x"], self.states[self.current_state]["y"], True)
    Environment.add_global_hotkey_listener(self.activate_toggle)

  def start(self):
    super().start()
    self.container = Rectangle(
      self,
      self.states[self.current_state]["container_rect"],
      fill=self.states[self.current_state]["container_color"],
      opacity=self.states[self.current_state]["container_opacity"],
      hole_rect=self.states[self.current_state]["container_hole_rect"],
      rounded_corners=20
    )
    self.content = Rectangle(
      self,
      self.states[self.current_state]["content_rect"],
      fill=self.states[self.current_state]["container_color"],
      opacity=self.states[self.current_state]["content_opacity"],
      rounded_corners=20
    )

    open_content_rect = self.states["open"]["content_rect"]
    self.input_box = InputBox(
      self,
      x=open_content_rect[0] + 10,
      y=open_content_rect[1] + 10,
      width=open_content_rect[2] - 100,
      height=open_content_rect[3] - 60,
      color="white"
    )

    self.output_box = OutputBox(
      self,
      width=self.states[self.current_state]["text_rect"][2],
      height=self.states[self.current_state]["text_rect"][3],
      x=self.states[self.current_state]["text_rect"][0],
      y=self.states[self.current_state]["text_rect"][1],
      font_size=self.states[self.current_state]["text_size"],
      fill=self.states[self.current_state]["text_color"],
      opacity=self.states[self.current_state]["text_opacity"]
    )

    self.button = Button(
      self,
      x=self.states[self.current_state]["button_rect"][0],
      y=self.states[self.current_state]["button_rect"][1],
      width=self.states[self.current_state]["button_rect"][2],
      height=self.states[self.current_state]["button_rect"][3],
      text='COOK',
      action=self.on_button_click,
      background="#f9f871",
      color="#845ec2"
    )

  def update(self):
    super().update()
    
    if self.is_transitioning:
      if self.state_transition_timer < self.state_transition_time:
        self.state_transition_timer += self.delta_time
      else:
        self.is_transitioning = False
        if self.current_state == "open":
          self.on_opened()
        elif self.current_state == "closed":
          self.on_closed()


    t = min(self.state_transition_timer / self.state_transition_time, 1.0)

    self.lerp_text_handler.tick(self.delta_time)

    self.transform.position = Vector2([
      self.lerp_state_parameter("x", t),
      self.lerp_state_parameter("y", t)
    ])

    if self.container is not None:
      self.container.fill = self.lerp_state_parameter("container_color", t)
      self.container.opacity = self.lerp_state_parameter("container_opacity", t)

      self.container.shape_data = self.lerp_state_parameter("container_rect", t)
      self.container.hole_rect = self.lerp_state_parameter("container_hole_rect", t)
      if self.content is not None:
        content_rect = self.lerp_state_parameter("content_rect", t)
        self.content.shape_data = content_rect
        self.content.fill = self.container.fill
        self.content.opacity = self.lerp_state_parameter("content_opacity", t)

        if self.input_box is not None:
          self.input_box.transform.width = int(content_rect[2])
          self.input_box.transform.height = int(content_rect[3])

      button_rect = self.lerp_state_parameter("button_rect", t)
      if self.button is not None:
        self.button.transform.local_position = button_rect[0:2]
        self.button.transform.width = int(button_rect[2])
        self.button.transform.height = int(button_rect[3])

    if self.output_box is not None:
      text_rect = self.lerp_state_parameter("text_rect", t)
      # print(f"Updating output box geometry to: {text_rect}")
      self.output_box.transform.local_position = text_rect[0:2]
      self.output_box.transform.width = int(text_rect[2])
      self.output_box.transform.height = int(text_rect[3])
      self.output_box.text = self.lerp_text_handler.text
      self.output_box.font_size = self.lerp_state_parameter("text_size", t)
      self.output_box.opacity = self.lerp_state_parameter("text_opacity", t)

  def add_submit_listener(self, listener):
    self.on_submit_event.add_listener(listener)

  def remove_submit_listener(self, listener):
    self.on_submit_event.remove_listener(listener)

  def change_state(self, new_state):
    if new_state not in self.states or new_state == self.current_state:
      return

    self.state_transition_timer = 0.0
    self.is_transitioning = True
    self.previous_state = self.current_state
    self.current_state = new_state
    if self.current_state == "open":
      self.qt_obj.set_inputs(True)
    else:
      self.input_box.hide()
      self.qt_obj.set_inputs(False)


  def activate_toggle(self):
    if time.time() - self.last_activation_time < 0.5:
      return
    self.last_activation_time = time.time()
    self.change_state("open" if self.current_state == "closed" else "closed")

  def on_opened(self):
    self.input_box.show()

  def on_closed(self):
    self.qt_obj.set_inputs(False)

  def on_button_click(self, _):
    self.on_submit_event.invoke(self.input_box.text)
    self.change_state("submitted")

  def on_response(self, response):
    self.lerp_text_handler.text = response


  def lerp_state_parameter(self, parameter, t):
    if t >= 1.0:
      return self.states[self.current_state][parameter]
    else:
      if isinstance(self.states[self.current_state][parameter], (int, float)):
        return (1 - t) * self.states[self.previous_state][parameter] + t * self.states[self.current_state][parameter]
      elif isinstance(self.states[self.current_state][parameter], str):
        # Attempt to interpolate between two color strings
        try:
          previous_color = QColor(self.states[self.previous_state][parameter])
          current_color = QColor(self.states[self.current_state][parameter])
          return QColor(
            int((1 - t) * previous_color.red() + t * current_color.red()),
            int((1 - t) * previous_color.green() + t * current_color.green()),
            int((1 - t) * previous_color.blue() + t * current_color.blue())
          )
        except:
          return self.states[self.current_state][parameter]
      elif isinstance(self.states[self.current_state][parameter], list):
        return [
          (1 - t) * self.states[self.previous_state][parameter][i] + t * self.states[self.current_state][parameter][i]
          for i in range(len(self.states[self.current_state][parameter]))
        ]
      else:
        return self.states[self.current_state][parameter]