from engine.scene import Scene

from assets.objects.fren import Fren
from assets.objects.toast import Toast


if __name__ == "__main__":

  # Root object for all other objects to spawn from
  scene = Scene(True)

  # Create the fren object
  Fren(scene, 'hole_punch')

  scene.tk_obj.after(5000, lambda: Toast("Hi! Welcome to PUnity.", 5000))

  # Run the main loop
  scene.begin()