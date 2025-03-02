import numpy as np

# Expressions used to animate the face
expressions = {
  "slow_scan": [
    (
      {
        "look_target": {
          "target_value": np.array([0., 100., 1000.]),
          "speed_factor": 1.0
        },
        "eye_open_factor": {
          "target_value": 1.0,
          "speed_factor": 1.0
        },
        "blinking": {
          "enabled": True,
          "frequency_range": [100, 1000]
        }
      },
      1.0
    ),
    (
      {
        "eye_open_factor": {
          "target_value": 0.3,
          "speed_factor": 0.5
        },
        "blinking": {
          "enabled": False
        }
      },
      1.0
    ),
    (
      {
        "look_target": {
          "target_value": np.array([200., 200., 1000.]),
          "speed_factor": 0.3
        }
      },
      3.0
    ),
    (
      {
        "look_target": {
          "target_value": np.array([0., 200., 1000.]),
          "speed_factor": 0.3
        }
      },
      3.0
    ),
    (
      {
        "look_target": {
          "target_value": np.array([100., 100., 1000.]),
          "speed_factor": 0.5
        },
        "eye_open_factor": {
          "target_value": 1.0,
          "speed_factor": 1.0
        },
        "blinking": {
          "enabled": True
        }
      },
      2.0
    )
  ],
  "sleep": [
    (
      {
        "look_target": {
          "target_value": np.array([100., 100., 1000.]),
          "speed_factor": 0.7
        },
        "eye_open_factor": {
          "target_value": 0.6,
          "speed_factor": 0.3
        },
        "mouth_open_factor": {
          "target_value": 0.8,
          "speed_factor": 0.5,
        },
        "mouth_talking": {
          "speed_factor": 0.1
        },
        "blinking": {
          "enabled": True,
          "frequency_range": [30, 70]
        }
      },
      3.0
    ),
    (
      {
        "eye_open_factor": {
          "target_value": 0.3,
          "speed_factor": 0.1
        },
        "mouth_open_factor": {
          "target_value": 0.0,
          "speed_factor": 0.1
        },
        "blinking": {
          "frequency_range": [100, 200]
        }
      },
      3.0
    ),
    (
      {
        "eye_open_factor": {
          "target_value": 0.0,
          "speed_factor": 0.3
        },
      },
      0.5
    ),
    (
      {
        "eye_open_factor": {
          "target_value": 0.2,
          "speed_factor": 0.05
        },
      },
      2.0
    ),
    (
      {
        "eye_open_factor": {
          "target_value": 0.0,
          "speed_factor": 0.3
        },
      },
      0.5
    ),
    (
      {
        "eye_open_factor": {
          "target_value": 0.1,
          "speed_factor": 0.3
        },
        "blinking": {
          "enabled": False,
        }
      },
      0.5
    ),
    (
      {
        "look_target": {
          "target_value": np.array([100., 200., 1000.]),
          "speed_factor": 0.1
        },
        "look_target": {
          "speed_factor": 1.0
        },
        "eye_open_factor": {
          "target_value": 0.0,
          "speed_factor": 0.01
        },
        "mouth_open_factor": {
          "speed_factor": 1.0,
        },
        "mouth_talking": {
          "speed_factor": 1.0
        },
        "blinking": {
          "enabled": True,
          "frequency_range": [100, 1000]
        },
        "face_scale": {
          "target_value": 0.2,
          "speed_factor": 0.1
        },
      },
      1.0
    )
  ],
  "wake": [
    (
      {
        "look_target": {
          "target_value": np.array([100., 100., 1000.]),
          "speed_factor": 1.0
        },
        "face_scale": {
          "target_value": 1.0,
          "speed_factor": 0.1
        },
        "face_position": {
          "target_value": np.array([100., 100., 0]),
          "speed_factor": 0.2
        },
      },
      0.5
    ),
    (
      {
        "eye_open_factor": {
          "target_value": 0.5,
          "speed_factor": 0.005
        },
      },
      3.0
    ),
    (
      {
        "blinking": {
          "enabled": True,
          "frequency_range": [10, 50]
        },
      },
      2.0
    ),
    (
      {
        "eye_open_factor": {
          "target_value": 1.0,
          "speed_factor": 0.6
        },
        "blinking": {
          "enabled": True,
          "frequency_range": [100, 1000]
        },
      },
      1.0
    ),
  ]
}