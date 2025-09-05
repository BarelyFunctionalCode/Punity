from engine.scene import Scene

from assets.objects.fren import Fren

if __name__ == "__main__":

  # Root object for all other objects to spawn from
  scene = Scene(True)

  # Create the fren object
  Fren(scene)

  # Run the main loop
  scene.begin()