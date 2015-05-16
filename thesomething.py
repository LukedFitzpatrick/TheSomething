import pygame
from pygame.locals import *
from random import *
from engineConstants import *
from graphics import *
from tile import *
from player import *
from math import *
import math
from levels import *
from trace import *



def displayGrid(surface, grid):
   for x in range(0, NUM_LEVEL_TILES_X):
        for y in range(0, NUM_LEVEL_TILES_Y):
            surface.blit(grid[x][y].sprite, ((x*TILE_WIDTH), (y*TILE_HEIGHT)))
            if BOUNDING_BOX_ON:
               pygame.draw.rect(surface, (100, 100, 100) , 
                  (x*TILE_WIDTH,y*TILE_HEIGHT,TILE_WIDTH,TILE_HEIGHT), 1)


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
   if TRACE_ON:
      traces = []
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

      if K_ESCAPE in keysDown:
         pygame.quit()
      keysDown = player.handleInput(keysDown)
      
      player.update()
      player.handleCollisions(currentGrid)
      
      displayGrid(windowSurface, currentGrid)

      if TRACE_ON:
         newTrace = Trace(windowSurface, 0, 250, 4, player.x + player.width/2, player.y + player.height/2)
         traces.append(newTrace)
         for trace in traces:
            if not trace.alive: traces.remove(trace)
            else: trace.update() 
      
      player.display()

      pygame.display.update()



pygame.init()
clock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN, 0)
windowSurface.fill((255, 255, 255))
player = Player( windowSurface, spritePlayerWalking, 32, 60, 0, 0, 16, 32, 50)

playGame(player, 1)
