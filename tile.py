from graphics import *
from engineConstants import *

class Tile:
   def __init__(self, sprite, isSolid):
      self.sprite = sprite
      self.isSolid = isSolid

blank = Tile(blankSpace, False)
solid = Tile(genericSolid, True)