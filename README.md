# PUnity

Unity, but in Python? Using Tkinter as a graphics base

# Road to 1.0 demo

- A hole appears after that part of the screen falls away in pieces
- Fren appears in hole and comes out
- When a non-fullscreen window is opened, it gets Fren's attention
- He phases into the window and disappears
- Period where the window shows various glitches
- Lifting up the bottom of the window like a garage door, Fren exits
- When the window comes back down it is greyed out and has a popup window on it

## TODO

### Features

- Object layer management
  - Layers: Background, Foreground, Top
- Program detection and tracking
  - Detect when a new application on the PC is started
  - Keep track of running applications with their window sizes and positions
- Fren Fade In/Out

### Objects

- Screen Chunk
  - Layer: Top
  - Inputs: polygon, position
  - Process:
    - Determine the size of the window based on the min/max coordinates of the polygon
    - Take a screenshot of the screen
    - crop the screenshot based on the polygon
    - Create canvas with an image of the clipped screenshot
- Hole
  - Layer: Background
  - Inputs: polygon, position, lifespan
  - Process:
    - Determine the size of the window based on the min/max coordinates of the polygon
    - Create canvas with the polygon (or maybe an image of a shadow gradient cropped to the polygon)
    - After lifespan is reached, fade out Hole and then destroy

### Effects

- Hole Punch (Duplicate screen section + Hole)
  - Inputs: polygon, position, lifespan
  - Objects:
    - Hole
    - Screen Chunk (+ Rigidbody): Gravity enabled and no collision
  - Process:
    - Break polygon into sections
    - Spawn Screen Chunks for sections
    - Spawn Hole for whole polygon
    - After Screen Chunks are off screen, destroy them
    - After Hole and Screen Chunks are gone, destroy self