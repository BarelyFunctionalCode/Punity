import Quartz

from utils import Vector2

def get_applications():
  windows = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListExcludeDesktopElements | Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)
  applications = []

  for window in windows:
    title = window[Quartz.kCGWindowName]
    width = window[Quartz.kCGWindowBounds]['Width']
    height = window[Quartz.kCGWindowBounds]['Height']
    x = window[Quartz.kCGWindowBounds]['X']
    y = window[Quartz.kCGWindowBounds]['Y']

    if y > 0 and width > 100 and height > 100 and title != "" and title != 'Notification Center' and "punity_" not in title:
      applications.append({
        'title': title,
        'position': Vector2([x, y]),
        'size': Vector2([width, height])
      })

  return applications
