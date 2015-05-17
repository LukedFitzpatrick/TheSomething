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
from agent import *
import random
from object import *

def displayRageGauge(surface, rage):
   barWidth = int((rage * BOTTOM_BAR_WIDTH) / 100)
   # draw the background
   pygame.draw.rect(surface, (200, 200, 200) , (0,BOTTOM_BAR_START,BOTTOM_BAR_WIDTH,BOTTOM_BAR_HEIGHT), 0)
   # draw the gauge
   pygame.draw.rect(surface, (230, 0, 0), (0, BOTTOM_BAR_START, int(barWidth), BOTTOM_BAR_HEIGHT), 0)

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
   keysDown, agents, objects = [], [], []

   for i in range(0, 1):
      tempAgent = Agent( windowSurface, spriteGenericAgent, randrange(40, 500), randrange(60, 100), 0, 0, 8, 16)
      agents.append(tempAgent)
   
   if TRACE_ON:
      traces = []
   
   counter = 150

   while not gameFinished:
      time_passed = clock.tick(FRAME_RATE)

      # spawn agents
      if(counter == 800):   
         tempAgent = Agent( windowSurface, spriteGenericAgent, 
            random.choice([GAME_SCREEN_WIDTH-100]), 32, 0, 0, 8, 16)
         agents.append(tempAgent)
         counter = 0
      else:
         counter += 1

      # handle keypresses
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


      # pass the keys down to the player to handle
      keysDown = player.handleInput(keysDown)
      
      # update the player and agents
      player.update()
      player.handleCollisions(currentGrid)
      #if(player.justChangedDirection):
         #if(player.xv > 0):
            #objects = particlePuff(windowSurface, spriteParticle, 4, 
            #   player.x+player.width, player.y+player.height, objects, 1)
         #elif(player.xv < 0):
            #objects = particlePuff(windowSurface, spriteParticle, 4,
            # player.x, player.y+player.height, objects, -1)

      for agent in agents:
         agent.handleSituation(player)
         agent.update()
         agent.handleCollisions(currentGrid)

      # display the grid
      displayGrid(windowSurface, currentGrid)

      # display traces
      if TRACE_ON:
         for agent in agents:
            newTrace = Trace(windowSurface, 0, 200, 30, agent.x + agent.width/2, agent.y + agent.height/2)
            traces.append(newTrace)
         for trace in traces:
            if not trace.alive: traces.remove(trace)
            else: trace.update()     
      
      # display the players, objects and agents
      player.display()
      
      # display objects
      for object in objects:
         if(not object.alive):
            objects.remove(object)
         else:
            object.update()

      # display agents, handle collisions between player/agents
      for agent in agents:
         agent.display()
         if(player.collisionBlock <= 0):
            if agent.getRect().collides(player.getRect()):
               tempObject = Object(windowSurface, spriteAnnoy, player.x+15, player.y-32, 15, 1, 0, 0, 0.1)
               objects.append(tempObject)
               player.annoy()
      

      # display the rage gauge
      displayRageGauge(windowSurface, player.rage)
      
      pygame.display.update()



pygame.init()
clock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN, 0)
windowSurface.fill((255, 255, 255))
player = Player( windowSurface, spritePlayerWalking, 32, 60, 0, 0, 16, 22, 50)

playGame(player, 1)
