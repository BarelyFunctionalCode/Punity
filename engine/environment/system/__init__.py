import platform

if platform.system() == 'Windows':
  # from .windows import get_applications
  pass
else:
  from .macos import add_input_event_monitor