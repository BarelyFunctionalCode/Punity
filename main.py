from engine.scene import Scene

from assets.objects.fren import Fren
from assets.effects.sticky_app_modal import StickyAppModal


if __name__ == "__main__":

  # Root object for all other objects to spawn from
  scene = Scene(True)

  # Create the fren object
  Fren(scene, 'hole_punch')

  StickyAppModal(
    scene,
    'Finder',
    400, 200,
    title='Uh Oh',
    text_content='Tomfoolery is afoot. Shit got fukd.',
    buttons=[
      {
        'text': 'Damn',
      },
    ]
  )

  # Run the main loop
  scene.begin()