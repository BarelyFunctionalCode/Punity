from objects.scene import Scene
from objects.fren import Fren

if __name__ == "__main__":

  # Root object for all other objects to spawn from
  scene = Scene(True)

  # Create the fren object
  Fren(scene, 'hole_punch')

  # Run the main loop
  scene.begin()