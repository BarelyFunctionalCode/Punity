# PUnity

Unity, but in Python?

This project is geared towards creating UI experiences not bound to an application window, or at least make it look that way.

Using Tkinter (tcl-tk) as the base for making graphics, and a similar structure and workflow as Unity, you can create anything from a persistant customized menu, an overlay for another program, or even a full-blown video game.

## Project Structure

- **main.py** - The obvious entrypoint, where the Scene is initialized along with any other objects to be spawned in at launch.

- **environment** - Keeps track of the overall usable size to have objects in, tracks mouse and keyboard inputs, and tracks telemetry on other applications running.

  - **external_application** - Collection of functions used to track other applications running on the system.

    - **macos.py** - Uses Quartz bindings to enumerate running applications on MacOS.

    - **windows.py** - TODO
  
- **base** - Folder for all base classes and other pieces that should general remain untouched unless you have a good reason.

  - **Component.py** - Used for the base of object.py and anything in the `assets/components` folder, which allows for user-created objects to use multiple inheritence to select whichever components apply for their object. This class is responsible for storing any shared functions that span all objects and components.

  - **object.py** - The base class used for all user-created object. This class facilitates the creation of the underlying Tk objects as well as runs the Update loop and collision detection for all objects.

  - **transform.py** - Used by the `Object` class to manage positional and size data for all objects.

  - **scene** - Class used to create the root Tk Window and the collision objects for the screen border. Also houses the `Editor` class.

    - **border.py** - A meta object of sorts thats used to add collision detection to the edges of the screen.

    - **editor** - Collection of inspection and testing tools used in the development process.

      - **control_menu.py** - Houses the controls for pausing/playing, adjusting the timescale, and toggling the `Hierarchy` and `Inspector` windows.

      - **hierarchy.py** - A sidebar that lists and shows the relationships of all the objects in the scene. Also, by selecting an item in the list you can populate the `Inspector` window with the details of the selected object.

      - **inspector.py** - A sidebar that shows the details about a selected object. By the powerers of python black magic, the `Insoector` will take a selected object, look up all the variables defined in the child and base classes, and display the current values of those variables broken up in sections by class. NOTE: This only shows variables that are defined in a given class's `__init__` function.

- **assets** - Where all the user-defined classes live.

  - **components** - Base classes used to add predefined logic to user-defined objects.

    - **rigidbody.py** - Managed a physics simulation on a given object and allows you to apply directional force to said object.

  - **objects** - Anything that gets spawned and rendered on-screen.

    - **hole.py** - Creates a black hole on-screen defined by the inputs.
      - Inputs:
        - hole_polygon - Collection of verticies that defines the shape of the hole to create.
        - x - x position.
        - y - y position.
        - lifetime - An optional value that defines when the hole despawns.

    - **screen_chunk.py** - Creates a copy of a portion of the screen defined by the inputs.
      - Inputs:
        - polygon - Collection of verticies that defines the shape of the chunk..
        - x - x position.
        - y - y position.
        - lifetime - An optional value that defines when the hole despawns.
        - is_static - Dictates if the object is meant to move or not.
        - invert_size - If defined, determines the size of the screen chunk with the polygon shape being cut out of the chunk.
        - invert_point - The x,y position where the polygon cutout is relative in the invert_size box.
    
    - **terminal.py** - A retro style terminal window used to output text.
      - Inputs:
        - x - x position.
        - y - y position.
        - update_queue - A python `Queue` object provided to allow an input stream used to output the text on the terminal.
  
  **effects** - Classes that are collections of objects that are executed in a predefined sequence.

    - **hole_punch.py** - Uses the `Hole` and `ScreenChunk` objects to visually create a chunk of the screen break out and fall to the ground, leaving a hole behind.
      - Inputs:
        - hole_polygon - Collection of verticies that defines the shape of the hole/chunk to create.
        - x - x position.
        - y - y position.
        - lifetime - An optional value that defines when the hole despawns.
        - collision_enabled - Determines if the resulting `ScreenChunk` produces collision events.

## Creating a new Object

In order to create a new object you need to use the `Object` base class and at the bare minumum have an `__init__` function that ends with calling `super().__init__(parent, "OBJECT NAME")`. The other parameters (`width`, `height`, `x`, `y`, `is_static`) are optional and can be set as needed.
```
class NewObject(Object):
  def __init__(self):
    name = "NewObject"
    width = 100
    height = 100
    x = 0
    y = 0
    is_static = True
    super().__init__(parent, name, width, height, x, y, is_static)
```

The following functions are defined in the base class `Object` and need to contain the relevant `super` calls in them.

### start

This function is called once immediately after the `__init__` and before the `update` function.

### update

The update loop of the object, called directly after `start` and runs roughly every 10ms. Anything time-based within the update function should utilize the `self.delta_time` variable to get the time elasped since the last update loop.

### on_collision

The function is called for any object that has `self.collision_enabled` set to `True` and provides all the relevant data for said collision. Use this function to add additional logic to the existing collision handling.















-----------------------------------









# Road to 1.0 demo

- A hole appears after that part of the screen falls away in pieces
- Fren appears in hole and comes out (done)
- When a non-fullscreen window is opened, it gets Fren's attention
- He phases into the window and disappears
- Period where the window shows various glitches
- Lifting up the bottom of the window like a garage door, Fren exits
- When the window comes back down it is greyed out and has a popup window on it

## TODO

### Features

- Object layer management
  - Layers: Background, Foreground, Top (done)
- Program detection and tracking
  - Detect when a new application on the PC is started
  - Keep track of running applications with their window sizes and positions
- Fren Fade In/Out

### Objects

- Screen Chunk (done)
  - Layer: Top
  - Inputs: polygon, position
  - Process:
    - Determine the size of the window based on the min/max coordinates of the polygon
    - Take a screenshot of the screen
    - crop the screenshot based on the polygon
    - Create canvas with an image of the clipped screenshot
- Hole (done)
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