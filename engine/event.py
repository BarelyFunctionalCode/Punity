from typing import Callable, List


class Event:
  """
  A class to manage event listeners and invoke them with arguments.
  Methods:
    add_listener(listener: Callable) -> None:
      Adds a listener (callable) to the list of listeners.
    remove_listener(listener: Callable) -> None:
      Removes a listener (callable) from the list of listeners.
      Raises a ValueError if the listener is not found.
    invoke(*args, **kwargs) -> None:
      Invokes all listeners in the list with the provided arguments.
  """

  def __init__(self):
    self.listeners: List[Callable] = []

  def add_listener(self, listener: Callable) -> None:
    """
    Registers a new listener to the event.

    Args:
      listener (Callable): A callable object (e.g., function or method) 
        that will be invoked when the event is triggered.
    """
    self.listeners.append(listener)
  
  def remove_listener(self, listener: Callable) -> None:
    """
    Removes a listener from the event's list of listeners.

    Args:
      listener (Callable): The listener function to be removed.

    Raises:
      ValueError: If the specified listener is not found in the list of listeners.
    """
    if listener in self.listeners:
      self.listeners.remove(listener)
    else:
      raise ValueError("Listener not found in the event listeners.")
    
  def invoke(self, *args, **kwargs) -> None:
    """
    Invokes all registered listeners with the provided arguments.

    This method iterates through the list of listeners and calls each one,
    passing along any positional and keyword arguments provided.

    Args:
      *args: Variable length argument list to pass to the listeners.
      **kwargs: Arbitrary keyword arguments to pass to the listeners.
    """
    for listener in self.listeners:
      try:
        listener(*args, **kwargs)
      except Exception as e:
        raise e