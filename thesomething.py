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
import time
from time import sleep
from object import *

def displayRageGauge(surface, rage):
   barWidth = int((rage * BOTTOM_BAR_WIDTH) / 100)
   # draw the background
   pygame.draw.rect(surface, (200, 200, 200) , (0,BOTTOM_BAR_START,BOTTOM_BAR_WIDTH,BOTTOM_BAR_HEIGHT), 0)
   # draw the gauge
   pygame.draw.rect(surface, (230, 0, 0), (0, BOTTOM_BAR_START, int(barWidth), BOTTOM_BAR_HEIGHT), 0)

   myfont = pygame.font.Font("font/ARCADECLASSIC.ttf", 30)
   text = str(int(rage))
   label = myfont.render(text, 1, (230, 0, 0))
   textpos = label.get_rect()
   textpos.centerx = barWidth + 20
   textpos.centery = int(BOTTOM_BAR_START + BOTTOM_BAR_HEIGHT/2)
   surface.blit(label, textpos)

def displayGrid(surface, grid, onlySolid = False):
   for x in range(0, NUM_LEVEL_TILES_X):
        for y in range(0, NUM_LEVEL_TILES_Y):
            if(onlySolid and not grid[x][y].isSolid):
               pass
            else:
               surface.blit(grid[x][y].sprite, ((x*TILE_WIDTH), (y*TILE_HEIGHT)))
            if BOUNDING_BOX_ON:
               pygame.draw.rect(surface, (100, 100, 100) , 
                  (x*TILE_WIDTH,y*TILE_HEIGHT,TILE_WIDTH,TILE_HEIGHT), 1)

def createMagnet(surface, player):
   magnet = Object(surface, spriteMagnet, player.x, player.y, MAGNET_DURATION, 2, 0, 0, 0)
   return magnet

def createVoid(surface, player):
   void = Object(surface, spriteVoid, player.x, player.y, VOID_DURATION, 2, 0, 0, 0)
   return void

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

def countDown(surface, number):
   myfont = pygame.font.Font("font/ARCADECLASSIC.ttf", 80)
   label = myfont.render(str(number), 1, (0, 0, 0))
   textpos = label.get_rect()
   textpos.centerx = GAME_SCREEN_WIDTH/2
   textpos.centery = GAME_SCREEN_HEIGHT/2
   surface.blit(label, textpos)
   pygame.display.update()
   sleep(1)

def playGame(player, level):
   currentGrid = generateGrid(level)
   agents = generateAgents(level, windowSurface)
   gameFinished = False
   keysDown,objects = [],[]
   
   if TRACE_ON:
      traces = []
   
   FRAME_RATE = FAST_RATE
   hasMagnet = False
   hasSmokescreen = False
   hasVoid = False
   smokeScreenCounter = 0
   objectMagnet = 0
   objectVoid = 0
   player.rage = 50
   
   frame_count = 0
   frame_rate = 0

   agentSpawnCounter = AGENT_SPAWN_FRAMES
   
   # do the initial countdown
   for i in range(3, 0, -1):
      displayGrid(windowSurface, currentGrid)
      player.display()
      for agent in agents:
         agent.display(player)
      
      countDown(windowSurface, i)
   
   displayGrid(windowSurface, currentGrid)
   player.display()
   for agent in agents:
      agent.display(player)
   countDown(windowSurface, "Begin")


   while not gameFinished:
      time_passed = clock.tick_busy_loop(FRAME_RATE)      


      if player.rage >= 100 or player.rage <= 0:
         gameFinished = True
      if(agentSpawnCounter <= 0):
         tempAgent = Agent( windowSurface, spriteGenericAgent, 
         random.choice([100, GAME_SCREEN_WIDTH-100]), 32, 0, 0, AGENT_WIDTH, AGENT_HEIGHT)
         agents.append(tempAgent)
         agentSpawnCounter = AGENT_SPAWN_FRAMES
      else:
         agentSpawnCounter -= 1

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
         if player.glyphs[GLYPH_MAGNET].active and not hasMagnet:
            objectMagnet = createMagnet(windowSurface, player)
            objects.append(objectMagnet)
            hasMagnet = True
         if player.glyphs[GLYPH_SMOKESCREEN].active:
            if not hasSmokescreen:
               hasSmokescreen = True
               smokeScreenCounter = SMOKE_SCREEN_DURATION
               player.sprite = spriteSmokescreenPlayer
         if player.glyphs[GLYPH_FIRE].active:
            objectFire = createFire(windowSurface, player)
            objects.append(objectFire)

         if player.glyphs[GLYPH_VOID].active and not hasVoid:
            objectVoid = createVoid(windowSurface, player)
            objects.append(objectVoid)
            hasVoid = True

         if player.glyphs[GLYPH_NUKE].active:
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
      if player.glyphs[GLYPH_SMOKESCREEN].active:
         if smokeScreenCounter > 0:
            smokeScreenCounter -= 1
         if smokeScreenCounter == 0:
            player.sprite = spritePlayerWalking
            hasSmokescreen = False

      player.handleCollisions(currentGrid)

      for agent in agents:           
         if hasMagnet:
            tempPlayerX, tempPlayerY = player.x, player.y
            player.x, player.y = objectMagnet.x, objectMagnet.y           
            agent.handleSituation(player)
            player.x, player.y = tempPlayerX, tempPlayerY
         
         elif hasVoid:
            tempPlayerX, tempPlayerY = player.x, player.y
            player.x, player.y = objectVoid.x, objectVoid.y           
            agent.handleSituation(player)
            player.x, player.y = tempPlayerX, tempPlayerY

         else:
            if ((hasSmokescreen) and math.fabs(player.x - agent.x) <= AGENT_LOS and 
               math.fabs(player.y - agent.y) <= AGENT_LOS):
               agent.xv = 0
               agent.yv = 0
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
            


      # display agents, handle collisions between player/agents
      close = False
      for agent in agents:
         agent.display(player)
         if(not close and player.closeTo(agent)):
            close = True
         if(player.collisionBlock <= 0 and not hasSmokescreen):
            # player agent collision
            if agent.getRect().collides(player.getRect()):
               (agent.xv, player.xv) = (2*player.xv, agent.xv/2)
               (agent.yv, player.yv) = (2*player.yv, agent.yv/2)
               
               # make the exclamation mark
               objects = makeAnnoySymbol(windowSurface, player, objects) 
               # annoy the player
               player.annoy()
               # if they have armor, sometimes kill the agent
               if player.glyphs[GLYPH_ARMOUR].active:
                  if randrange(1, ARMOUR_KILL_FREQUENCY) == 1:
                     player.armourKill()
                     agent.alive = False
               if player.glyphs[GLYPH_CHARGE].active and player.charging:
                  agent.alive = False
                  player.chargeKill()
               # check for infection glyph, infect this monster
               if player.glyphs[GLYPH_INFECTION].active and agent.infectionCounter == -1:
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

      displayGrid(windowSurface, currentGrid, True)
      # display objects
      for object in objects:
         if(not object.alive):
            if object is objectMagnet:
               hasMagnet = False
            if object is objectVoid:
               hasVoid = False
            objects.remove(object)
         
         else:
            object.update()
         
         if(object.sprite is spriteFire):
            for agent in agents:
               if agent.getRect().collides(object.getRect()):
                  agent.alive = False
                  player.fireKill()
         if(object.sprite is spriteVoid):
            for agent in agents:
               if agent.getRect().collides(object.getRect()):
                  agent.alive = False
                  player.voidKill()

      # display just the agents again so the circles don't overlap them.
      for agent in agents:
         agent.display(player, True)

      player.display()

      FRAME_RATE = FAST_RATE
      if player.glyphs[GLYPH_BULLET_TIME].active:
         if close:
            FRAME_RATE = SLOW_RATE
         

      # display the rage gauge
      displayRageGauge(windowSurface, player.rage)
      displayGlyphs(windowSurface, player)
      pygame.display.update()

   
   if(player.rage >= 100):
      return False
   if(player.rage <= 0):
      return True

def displayTextBox(text, colour, line = 0):
    myfont = pygame.font.Font("font/ARCADECLASSIC.ttf", 30)
   
    # render text
    label = myfont.render(text, 1, colour)
    textpos = label.get_rect()
    textpos.centerx = windowSurface.get_rect().centerx
    textpos.centery = 20 + line*35
    windowSurface.blit(label, textpos)


def chooseGlyphsScreen(surface, player):
   pygame.draw.rect(windowSurface, (0, 0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 0)
   myfont = pygame.font.Font("font/ARCADECLASSIC.ttf", 30)

   glyphsSelected = 0
   finished = False
   keysDown = []
   while (not finished):
      for event in pygame.event.get():
         if event.type == QUIT: 
            pygame.quit()
         elif event.type == pygame.KEYDOWN: 
            keysDown.append(event.key)
         elif event.type == pygame.KEYUP: 
            if(event.key in keysDown):
               keysDown.remove(event.key)

      if(K_RETURN in keysDown): finished = True
      if(K_ESCAPE in keysDown): pygame.quit()
      
      availableCount = 0
      for glyph in player.glyphs:
         if glyph.available:
            availableCount += 1

      # update the glyphs on keypress    
      for glyph in player.glyphs:
         if(glyph.selectionKey in keysDown) and glyph.unlocked:
            keysDown.remove(glyph.selectionKey)
            if not glyph.available:
               if(availableCount < 3):
                  glyph.available = True
            elif glyph.available:
               glyph.available = False

      pygame.draw.rect(windowSurface, (0, 0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 0)
      displayTextBox("GLYPH SELECTION      ", (255, 255, 255), 0)
      line = 1
      for glyph in player.glyphs:
         if not glyph.unlocked: 
            displayTextBox("LOCKED ", (255, 255, 255), line)
         else: 
            displayTextBox(glyph.name, glyph.getTextColour(), line)
         line += 1      

      pygame.display.flip()

   setActive = False
   for glyph in player.glyphs:
      if not setActive and glyph.available:
         glyph.active = True
         setActive = True
      else:
         glyph.active = False

def displayGlyphs(surface, player):
   pygame.draw.rect(windowSurface, (0, 0, 0), (0, GLYPHLOCATIONY, SCREEN_WIDTH, GLYPH_HEIGHT), 0)
   index = 0
   for glyph in player.glyphs:
      if(glyph.available):
         glyph.sprite.blit(surface, (GLYPHLOCATIONX + GLYPH_WIDTH*index, GLYPHLOCATIONY))
         if glyph.active:
            pygame.draw.rect(surface, (255, 0, 0) , (GLYPHLOCATIONX + GLYPH_WIDTH*index,GLYPHLOCATIONY,GLYPH_WIDTH,GLYPH_HEIGHT), 2)
         index += 1

pygame.init()
clock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 0)
windowSurface.fill((255, 255, 255))
player = Player( windowSurface, spritePlayerWalking, 500, 50, 0, 0, PLAYER_WIDTH, PLAYER_HEIGHT, 50)


while (True):
   #devScreen(windowSurface, player)
   chooseGlyphsScreen(windowSurface, player)
   playGame(player, 2)

   