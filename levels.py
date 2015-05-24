from tile import *
from graphics import *
from engineConstants import *
from agent import *
import random

def generateAgents(level, surface):
   agents = [] 
   for i in range(1, 5):
      tempAgent = Agent( surface, spriteGenericAgent, 
         random.choice([100, GAME_SCREEN_WIDTH-100]), 32, 0, 0, AGENT_WIDTH, AGENT_HEIGHT)
      agents.append(tempAgent)
   return agents


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

   if level == 1:

      for x in range(8, NUM_LEVEL_TILES_X-9):
         grid[x][15] = solid

      for x in range(0, 5):
         grid[x][12] = solid

      for x in range(NUM_LEVEL_TILES_X-6, NUM_LEVEL_TILES_X):
         grid[x][12] = solid
      
      for x in range(8, NUM_LEVEL_TILES_X-9):
         grid[x][8] = solid

      for x in range(0, 5):
         grid[x][4] = solid

      for x in range(NUM_LEVEL_TILES_X-6, NUM_LEVEL_TILES_X):
         grid[x][4] = solid

   elif level == 2:
      for x in range(3, 5):
         grid[x][NUM_LEVEL_TILES_Y - 4] = solid

      for x in range(7, 9):
         grid[x][NUM_LEVEL_TILES_Y - 6] = solid

   return grid