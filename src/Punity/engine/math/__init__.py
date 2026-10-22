from enum import Enum

from .vector2 import *
from .vector3 import *

###################################
########## Util Functions #########
###################################

def away_from_zero(x):
  return int(x // 1 + 2 ** (x > 0) - 1)

###################################
############# Enums ###############
###################################

class Side(Enum):
  TOP = 0
  RIGHT = 1
  BOTTOM = 2
  LEFT = 3
  FRONT = 4
  BACK = 5
