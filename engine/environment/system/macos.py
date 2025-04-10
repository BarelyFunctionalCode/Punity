import AppKit
import time

from engine.math import Vector2

def add_input_event_monitor(env, p_event):
  def handle_event(event: AppKit.NSEvent):
    event_data = {'timestamp': time.time()}
    if event.type() == AppKit.NSEventTypeMouseMoved:
      pos = AppKit.NSEvent.mouseLocation()
      pos_list = [pos.x, env.height - pos.y]
      env.mouse_position = Vector2(pos_list)
      event_data['type'] = 'mouse_move'
      event_data['position'] = pos_list
    elif event.type() == AppKit.NSEventTypeLeftMouseDown:
      pos = AppKit.NSEvent.mouseLocation()
      pos_list = [pos.x, env.height - pos.y]
      event_data['type'] = 'mouse_down'
      event_data['position'] = pos_list
    elif event.type() == AppKit.NSEventTypeKeyDown:
      event_data['type'] = 'key_down'
      event_data['key'] = event.characters()
    else:
      return

    # add event to queue
    p_event.invoke(event_data)

  # add global input event monitor
  AppKit.NSEvent.addGlobalMonitorForEventsMatchingMask_handler_(
    AppKit.NSEventMaskAny,
    handle_event
  )