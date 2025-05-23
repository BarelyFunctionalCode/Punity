import Quartz

from engine.math import Vector2

application_name_blacklist = [
  'Dock',
  'Control Center',
  'Notification Center',
]


def get_applications():
  windows = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListExcludeDesktopElements | Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)
  applications = []

  for window in windows:
    pid = window[Quartz.kCGWindowOwnerPID]
    number = window[Quartz.kCGWindowNumber]
    name = window[Quartz.kCGWindowOwnerName] 
    title = window[Quartz.kCGWindowName] if Quartz.kCGWindowName in window else ""
    width = window[Quartz.kCGWindowBounds]['Width']
    height = window[Quartz.kCGWindowBounds]['Height']
    x = window[Quartz.kCGWindowBounds]['X']
    y = window[Quartz.kCGWindowBounds]['Y']

    if name not in application_name_blacklist and y > 0 and width > 100 and height > 100 and title != "" and "punity_" not in title:
      applications.append({
        'pid': pid,
        'number': number,
        'name': name,
        'title': title,
        'size': Vector2([width, height]),
        'position': Vector2([x, y])
      })

  return applications