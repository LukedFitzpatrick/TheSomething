import pygame
from pygame.locals import *
from random import *
from engineConstants import *
from graphics import *
from tile import *
from player import *
from math import *
import math

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

   for y in range(13, 15):
      for x in range(6, 13):
         grid[x][y] = solid
   
   #grid[5][NUM_LEVEL_TILES_Y-1] = blank

   return grid

def displayPlayer(player):
   player.sprite.blit(windowSurface, (player.x, player.y))

def displayGrid(grid):
   for x in range(0, NUM_LEVEL_TILES_X):
        for y in range(0, NUM_LEVEL_TILES_Y):
            windowSurface.blit(grid[x][y].sprite, ((x*TILE_WIDTH), (y*TILE_HEIGHT)))

def waitForAnyKey():
   buttonPressed = False
   while buttonPressed == False:
      for event in pygame.event.get():
         if event.type == QUIT:
            pygame.quit()
         if event.type == pygame.KEYDOWN:
            buttonPressed = True


  
def playGame(player, level):
   currentGrid = generateGrid(level)
   gameFinished = False
   keysDown = []
   while not gameFinished:
      time_passed = clock.tick(FRAME_RATE)

      for event in pygame.event.get():
         if event.type == QUIT:
            pygame.quit()
         elif event.type == pygame.KEYDOWN:
            keysDown.append(event.key)
         elif event.type == pygame.KEYUP:
            if(event.key in keysDown):
               keysDown.remove(event.key)
      
      keysDown = player.handleInput(keysDown)
      
      player.update()
      player.handleCollisions(currentGrid)
      
      displayGrid(currentGrid)
      displayPlayer(player)

      pygame.display.update()



pygame.init()
clock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 0)
windowSurface.fill((255, 255, 255))
player = Player(spritePlayerWalking, 32, 60, 0, 0, 32, 32, 50)

playGame(player, 1)
