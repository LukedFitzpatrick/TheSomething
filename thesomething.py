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

def createMagnet(surface, player):
   magnet = Object(surface, spriteMagnet, player.x, player.y, MAGNET_DURATION, 2, 0, 0, 0)
   return magnet

def createFire(surface, player):
   fire = Object(surface, spriteFire, player.x, player.y, FIRE_DURATION, 0, 0, 0, 0)
   return fire


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


   
   if TRACE_ON:
      traces = []
   
   agentSpawnCounter = AGENT_SPAWN_FRAMES - 1
   FRAME_RATE = FAST_RATE
   hasMagnet = False
   hasSmokescreen = False
   smokeScreenCounter = 0
   objectMagnet = 0

   while not gameFinished:
      time_passed = clock.tick(FRAME_RATE)

      # spawn agents
      if(agentSpawnCounter == AGENT_SPAWN_FRAMES):   
         tempAgent = Agent( windowSurface, spriteGenericAgent, 
            random.choice([100, GAME_SCREEN_WIDTH-100]), 32, 0, 0, AGENT_WIDTH, AGENT_HEIGHT)
         agents.append(tempAgent)
         agentSpawnCounter = 0
      else:
         agentSpawnCounter += 1

      # handle keypresses
      for event in pygame.event.get():
         if event.type == QUIT:
            pygame.quit()
         elif event.type == pygame.KEYDOWN:
            keysDown.append(event.key)
         elif event.type == pygame.KEYUP:
            if(event.key in keysDown):
               player.handleKeyUp(event.key)
               keysDown.remove(event.key)
      if K_SPACE in keysDown:
         if GLYPH_MAGNET and not hasMagnet:
            objectMagnet = createMagnet(windowSurface, player)
            objects.append(objectMagnet)
            hasMagnet = True
         if GLYPH_SMOKESCREEN:
            if not hasSmokescreen:
               hasSmokescreen = True
               smokeScreenCounter = SMOKE_SCREEN_DURATION
               player.sprite = spriteSmokescreenPlayer
         if GLYPH_FIRE:
            objectFire = createFire(windowSurface, player)
            objects.append(objectFire)
         if GLYPH_NUKE:
            for agent in agents:
               agent.alive = False
               player.nukeKill()
                        
      if K_ESCAPE in keysDown:
         pygame.quit()


      # pass the keys down to the player to handle
      keysDown = player.handleInput(keysDown)
      
      # update the player and agents
      player.update()
      # update the smokescreen
      if GLYPH_SMOKESCREEN:
         if smokeScreenCounter > 0:
            smokeScreenCounter -= 1
         if smokeScreenCounter == 0:
            player.sprite = spritePlayerWalking
            hasSmokescreen = False

      player.handleCollisions(currentGrid)


      for agent in agents:
         if hasMagnet:
            tempPlayerX = player.x
            tempPlayerY = player.y
            player.x = objectMagnet.x
            player.y = objectMagnet.y

            agent.handleSituation(player)
            player.x = tempPlayerX
            player.y = tempPlayerY
         else:
            if(hasSmokescreen):
               #agent.xv = 0
               pass
               #agent.yv = 0
            else:
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
            if object is objectMagnet:
               hasMagnet = False
            objects.remove(object)
         
         else:
            object.update()
         if(object.sprite is spriteFire):
            for agent in agents:
               if agent.getRect().collides(object.getRect()):
                  agent.alive = False
                  player.fireKill()

         

      # display agents, handle collisions between player/agents
      close = False
      for agent in agents:
         agent.display()
         if(not close and player.closeTo(agent)):
            close = True
         if(player.collisionBlock <= 0 and not hasSmokescreen):
            # player agent collision
            if agent.getRect().collides(player.getRect()):
               # make the exclamation mark
               objects = makeAnnoySymbol(windowSurface, player, objects) 
               # annoy the player
               player.annoy()
               # if they have armor, sometimes kill the agent
               if GLYPH_ARMOUR:
                  if randrange(1, ARMOUR_KILL_FREQUENCY) == 1:
                     player.armourKill()
                     agent.alive = False
               if GLYPH_CHARGE and player.charging:
                  agent.alive = False
                  player.chargeKill()
               # check for infection glyph, infect this monster
               if GLYPH_INFECTION and agent.infectionCounter == -1:
                  agent.infect()
                  player.infectionKill()
         
         # try to promulgate the infection
         if(agent.infectionCounter > 0):
            for agent2 in agents:
               if agent.getRect().collides(agent2.getRect()) and agent2.infectionCounter == -1:
                  agent2.infect()
                  player.infectionKill()

         if not agent.alive:
            agents.remove(agent)

      if GLYPH_BULLET_TIME:
         if close:
            FRAME_RATE = SLOW_RATE
         else:
            FRAME_RATE = FAST_RATE

      # display the rage gauge
      displayRageGauge(windowSurface, player.rage)
      
      pygame.display.update()



pygame.init()
clock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN, 0)
windowSurface.fill((255, 255, 255))
player = Player( windowSurface, spritePlayerWalking, PLAYER_WIDTH, PLAYER_HEIGHT, 0, 0, 16, 22, 50)

playGame(player, 1)
