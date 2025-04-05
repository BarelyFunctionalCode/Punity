from typing import Callable, List


class Event:
  """
  Allows for the creation of events that can be listened to.
  Once invoked, all listeners will be called with the given arguments.
  """

  def __init__(self):
    """
    Initializes an empty event.
    """
    self.listeners: List[Callable] = []

  def add_listener(self, listener: Callable):
    """
    Adds a listener to the event.
    :param listener: The function to call when the event is triggered.
    """
    self.listeners.append(listener)
  
  def remove_listener(self, listener: Callable):
    """
    Removes a listener from the event.
    :param listener: The function to remove.
    """
    if listener in self.listeners:
      self.listeners.remove(listener)
    else:
      raise ValueError("Listener not found in the event listeners.")
    
  def invoke(self, *args, **kwargs):
    """
    Calls all listeners with the given arguments.
    :param args: Positional arguments to pass to the listeners.
    :param kwargs: Keyword arguments to pass to the listeners.
    """
    for listener in self.listeners:
      listener(*args, **kwargs)