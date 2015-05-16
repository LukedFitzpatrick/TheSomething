from tile import *
from graphics import *
from engineConstants import *

def generateGrid(level):
   grid = []
   for x in range(0, NUM_LEVEL_TILES_X):
      line = []
      for y in range(0, NUM_LEVEL_TILES_Y):
         if(x == 0 or x == NUM_LEVEL_TILES_X-1 or y == 0 or y == NUM_LEVEL_TILES_Y-1):
            line.append(solid)
         else:
            line.append(blank)
      grid.append(line)

   for x in range(6, NUM_LEVEL_TILES_X-7):
      grid[x][11] = solid
   
   return grid