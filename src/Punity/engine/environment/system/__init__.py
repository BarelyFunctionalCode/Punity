import platform

if platform.system() == 'Windows':
  from .windows import add_input_event_monitor
elif platform.system() == 'Darwin':
  from .macos import add_input_event_monitor
elif platform.system() == 'Linux':
  from .linux import add_input_event_monitor