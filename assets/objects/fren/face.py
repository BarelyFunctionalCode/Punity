from queue import Queue
import tkinter as tk
import numpy as np
import datetime as date

from .expressions import expressions


class TkinterFace:
  def __init__(self, obj, face_polygon):
    self.obj = obj
    self.tk_obj = obj.tk_obj
    self.face_polygon = face_polygon
    self.is_active = False
    self.is_enabled = True

    self.is_asleep = False

    self.width = self.tk_obj.winfo_width()
    self.height = self.tk_obj.winfo_height()

    # Canvas for drawing face
    self.graphic_canvas = tk.Canvas(self.tk_obj, width=self.width, height=self.height, bg=self.tk_obj['bg'], bd=0, highlightthickness=0, cursor='none')
    self.graphic_canvas.pack(padx=0, pady=0, side=tk.TOP)

    # Face Parameters
    self.face_parameters = {
      "look_target": {
        "current_value": np.array([self.width / 2, self.height / 3, 1000.0]),
        "target_value": np.array([self.width / 2, self.height / 3, 1000.0]),
        "max_speed": 20,
        "min_speed": 1,
        "speed_factor": 1.0
      },
      "eye_open_factor": {
        "current_value": 1.0,
        "target_value": 1.0,
        "max_speed": .1,
        "min_speed": .01,
        "speed_factor": 1.0
      },
      "mouth_open_factor": {
        "current_value": 0.0,
        "target_value": 0.0,
        "max_speed": .1,
        "min_speed": .01,
        "speed_factor": 1.0,
      },
      "mouth_talking": {
        "max_speed": 30.0,
        "min_speed": 1.0,
        "speed_factor": 1.0
      },
      "blinking": {
        "enabled": True,
        "frequency_range": [100, 1000]
      },
      "face_scale": {
        "current_value": 1.0,
        "target_value": 1.0,
        "max_speed": .1,
        "min_speed": .01,
        "speed_factor": 1.0,
      },
      "face_position": {
        "current_value": np.array([self.width / 2, 75.0, 0]),
        "target_value": np.array([self.width / 2, 75.0, 0]),
        "max_speed": 20,
        "min_speed": 1,
        "speed_factor": 1.0,
      },
    }

    self.current_expression = None

    self.face_update_timer = 0

    self.sleep_drift_direction = np.array([0.0, 0.0, 0.0])

    # Eyes
    self.pupil_movement_factor = 1.0
    self.blink_timer = 100

    # Objects
    self.eyes = [None, None]
    self.pupils = [None, None]
    self.mouth = None

    self.update_queue = Queue()
    self.talking_queue = Queue()
    self.talking_mouth_delay = 50
    self.talking_mouth_delay_timer = 0

  # Used to set the face expression
  def set_face_expression(self, expression):
    if expression in expressions:
      self.current_expression = expression

      for step, duration in expressions[expression]:
        self.update_queue.put((step, duration))
  
  # Adjust face parameter based on target value and speed
  def adjust_face_parameter(self, parameter):
    parameter_data = self.face_parameters[parameter]
    
    parameter_data["current_value"] = np.clip(
      (
        parameter_data["current_value"] +
        (
          np.sign(parameter_data["target_value"] - parameter_data["current_value"]) * (
            (
              (1 - parameter_data["speed_factor"]) * parameter_data["min_speed"] +
              parameter_data["speed_factor"] * parameter_data["max_speed"]
            )
          )
        )
      ),
      np.minimum(parameter_data["current_value"], parameter_data["target_value"]),
      np.maximum(parameter_data["current_value"], parameter_data["target_value"])
    )

  # Loop for updating the face
  def update(self):
    # Update mouth open factor from queue
    if self.talking_mouth_delay_timer > self.talking_mouth_delay and self.is_enabled and not self.talking_queue.empty():
      self.talking_mouth_delay_timer = 0
      self.face_parameters["mouth_open_factor"]["target_value"] = self.talking_queue.get()
    
    self.talking_mouth_delay_timer += self.obj.delta_time

    # Update face parameters from queue
    if not self.update_queue.empty():
      if self.is_enabled or self.is_asleep: self.is_active = True
      if (self.is_enabled or self.current_expression in ["sleep", "wake"]) and \
          self.face_update_timer <= date.datetime.now().timestamp():
        face_update, duration = self.update_queue.get()

        if self.current_expression == "sleep":
          self.is_enabled = False
          self.is_active = False
        if self.current_expression == "wake":
          self.is_asleep = False

        self.face_update_timer = date.datetime.now().timestamp() + duration

        for parameter_name in face_update:
          if parameter_name in self.face_parameters:
            for parameter_field in face_update[parameter_name]:
              if parameter_field in self.face_parameters[parameter_name]:
                if type(face_update[parameter_name][parameter_field]) == np.ndarray:
                  self.face_parameters[parameter_name][parameter_field] = np.array(face_update[parameter_name][parameter_field])
                else:
                  self.face_parameters[parameter_name][parameter_field] = face_update[parameter_name][parameter_field]

    # Clear out if current expression is finished and the update queue is empty
    if self.face_update_timer <= date.datetime.now().timestamp() and self.update_queue.empty():
      if self.current_expression == "sleep":
        self.is_asleep = True
      if self.current_expression == "wake": 
        self.is_enabled = True
      self.current_expression = None
      self.is_active = False

    # Update face parameters that can be customized
    for parameter_name in self.face_parameters:
      if "target_value" in self.face_parameters[parameter_name]:
        self.adjust_face_parameter(parameter_name)

    # Calulate how open the eyes are based on the eye open factor and blink timer
    eye_y = 4.0
    eye_open_value = eye_y
    if self.blink_timer > self.face_parameters["blinking"]["frequency_range"][1]:
      self.blink_timer = np.random.randint(*self.face_parameters["blinking"]["frequency_range"])
    if self.face_parameters["blinking"]["enabled"]:
      self.blink_timer -= 1
      if self.blink_timer < -eye_open_value:
        self.blink_timer = np.random.randint(*self.face_parameters["blinking"]["frequency_range"])
      elif self.blink_timer < 0:
        eye_open_value = min(eye_open_value - self.blink_timer, eye_y)
      elif self.blink_timer < eye_open_value:
        eye_open_value = max(self.blink_timer, 0)
    eye_open_value *= self.face_parameters["eye_open_factor"]["current_value"]

    # Eye size based on base parameters and eye open value
    eye_scale = 12.0 * self.face_parameters["face_scale"]["current_value"]
    eye_x = 2.75
    eye_size = np.array([eye_scale * eye_x, eye_scale * eye_open_value])
    eye_half_size = eye_size / 2

    # Keep the pupil within the eye
    pupil_radius = 10.0 * self.face_parameters["face_scale"]["current_value"]
    pupil_max_movement = np.array(eye_half_size - [pupil_radius, pupil_radius]).clip(0)

    # Calculate pupil position based on look direction
    look_direction = (
      (self.face_parameters["look_target"]["current_value"] - self.face_parameters["face_position"]["current_value"])) / \
      (np.linalg.norm(self.face_parameters["look_target"]["current_value"] - self.face_parameters["face_position"]["current_value"])
    )
    pupil_center = look_direction[:2] * eye_size * self.pupil_movement_factor
    pupil_center = np.clip(pupil_center, -pupil_max_movement, pupil_max_movement)

    # Eye position and generating oval coordinates for canvas
    eye_distance = 35.0 * self.face_parameters["face_scale"]["current_value"]
    eye_offset_pos = np.array([0,-30]) * self.face_parameters["face_scale"]["current_value"]
    eye_positions = [
      self.face_parameters["face_position"]["current_value"][:2] - np.array([eye_distance, 0]) + eye_offset_pos + (look_direction[:2] * 70.0),
      self.face_parameters["face_position"]["current_value"][:2] + np.array([eye_distance, 0]) + eye_offset_pos + (look_direction[:2] * 70.0)
    ]

    eye_ovals = [ (
      eye_position[0] - eye_half_size[0],
      eye_position[1] - eye_half_size[1],
      eye_position[0] + eye_half_size[0] + 1, # +1 because eye_half_size of zero leaves artifacts on the canvas
      eye_position[1] + eye_half_size[1] + 1
    ) for eye_position in eye_positions ]

    pupil_ovals = [ (
      eye_position[0] + pupil_center[0] - min(pupil_radius, eye_half_size[0]),
      eye_position[1] + pupil_center[1] - min(pupil_radius, eye_half_size[1]),
      eye_position[0] + pupil_center[0] + min(pupil_radius, eye_half_size[0]),
      eye_position[1] + pupil_center[1] + min(pupil_radius, eye_half_size[1])
    ) for eye_position in eye_positions ]


    # Represent mouth as a moving sine wave
    talking_speed = (
      self.face_parameters["mouth_talking"]["min_speed"] * (1.0 - self.face_parameters["mouth_talking"]["speed_factor"]) +
      (self.face_parameters["mouth_talking"]["max_speed"] * self.face_parameters["mouth_talking"]["speed_factor"])
    )
    sin_seed = date.datetime.now().timestamp() * talking_speed

    mouth_min_frequency = 2.5 * self.face_parameters["face_scale"]["current_value"]
    mouth_max_frequency = 10.0 * self.face_parameters["face_scale"]["current_value"]
    mouth_resolution = 100
    mouth_sine = np.sin(
      np.linspace(
        sin_seed,
        sin_seed + mouth_min_frequency + (mouth_max_frequency * self.face_parameters["mouth_open_factor"]["current_value"]),
        mouth_resolution
      )
    )
    mouth_amplitude = 25.0 * self.face_parameters["face_scale"]["current_value"] * self.face_parameters["mouth_open_factor"]["current_value"]
    mouth_sine = mouth_sine * mouth_amplitude

    # Calculate mouth position based on face position and mouth offset
    mouth_offset_pos = np.array([0, 45.0]) * self.face_parameters["face_scale"]["current_value"]
    mouth_center = np.array([0, 0])
    mouth_length = (50.0 + 50.0 * (1.0 - self.face_parameters["mouth_open_factor"]["current_value"])) * self.face_parameters["face_scale"]["current_value"]
    mouth_start = self.face_parameters["face_position"]["current_value"][:2] + mouth_offset_pos + mouth_center - np.array([mouth_length / 2, 0])

    def slope_mouth(x, value):
      return np.exp(-pow((x - (mouth_resolution / 2.0)) / (mouth_length / (3.0 - self.face_parameters["mouth_open_factor"]["current_value"])), 2.0)) * value

    # Generate mouth line coordinates for canvas based on points on the sine wave
    mouth_line = ()
    for i in range(int(mouth_resolution)):
      mouth_line += (
        mouth_start[0] + mouth_length * i / mouth_resolution,
        mouth_start[1] + slope_mouth(i, mouth_sine[i]),
      )

    # Draw Face
    if self.graphic_canvas.find_all() == ():
      self.graphic_canvas.create_polygon(*self.face_polygon, fill='#004400', stipple='gray75', smooth=True)
      self.eyes[0] = self.graphic_canvas.create_rectangle(eye_ovals[0], outline='green', width=4)
      self.eyes[1] = self.graphic_canvas.create_rectangle(eye_ovals[1], outline='green', width=4)
      self.pupils[0] = self.graphic_canvas.create_rectangle(pupil_ovals[0], outline='#008800', width=1, fill='#008800')
      self.pupils[1] = self.graphic_canvas.create_rectangle(pupil_ovals[1], outline='#008800', width=1, fill='#008800')
      self.mouth = self.graphic_canvas.create_line(mouth_line, fill='green', width=4)
    else:
      self.graphic_canvas.coords(self.eyes[0], eye_ovals[0])
      self.graphic_canvas.coords(self.eyes[1], eye_ovals[1])
      self.graphic_canvas.coords(self.pupils[0], pupil_ovals[0])
      self.graphic_canvas.coords(self.pupils[1], pupil_ovals[1])
      self.graphic_canvas.coords(self.mouth, mouth_line)