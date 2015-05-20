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
   hasVoid = False
   smokeScreenCounter = 0
   objectMagnet = 0
   objectVoid = 0
   player.rage = 50

   while not gameFinished:
      time_passed = clock.tick(FRAME_RATE)

      if player.rage >= 100 or player.rage <= 0:
         gameFinished = True


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
         if player.glyphs[GLYPH_MAGNET] and not hasMagnet:
            objectMagnet = createMagnet(windowSurface, player)
            objects.append(objectMagnet)
            hasMagnet = True
         if player.glyphs[GLYPH_SMOKESCREEN]:
            if not hasSmokescreen:
               hasSmokescreen = True
               smokeScreenCounter = SMOKE_SCREEN_DURATION
               player.sprite = spriteSmokescreenPlayer
         if player.glyphs[GLYPH_FIRE]:
            objectFire = createFire(windowSurface, player)
            objects.append(objectFire)

         if player.glyphs[GLYPH_VOID] and not hasVoid:
            objectVoid = createVoid(windowSurface, player)
            objects.append(objectVoid)
            #voidCounter = VOID_DURATION
            hasVoid = True

         if player.glyphs[GLYPH_NUKE]:
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
      if player.glyphs[GLYPH_SMOKESCREEN]:
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
               if player.glyphs[GLYPH_ARMOUR]:
                  if randrange(1, ARMOUR_KILL_FREQUENCY) == 1:
                     player.armourKill()
                     agent.alive = False
               if player.glyphs[GLYPH_CHARGE] and player.charging:
                  agent.alive = False
                  player.chargeKill()
               # check for infection glyph, infect this monster
               if player.glyphs[GLYPH_INFECTION] and agent.infectionCounter == -1:
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

      if player.glyphs[GLYPH_BULLET_TIME]:
         if close:
            FRAME_RATE = SLOW_RATE
         else:
            FRAME_RATE = FAST_RATE

      # display the rage gauge
      displayRageGauge(windowSurface, player.rage)
      
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


def devScreen(surface, player):
   pygame.draw.rect(windowSurface, (0, 0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 0)
   myfont = pygame.font.Font("font/ARCADECLASSIC.ttf", 30)
   
   # render text
   keysDown = []

   glyphsSelected = 0
   finished = False
   while (not finished):
      for event in pygame.event.get():
         if event.type == QUIT:
            pygame.quit()
         elif event.type == pygame.KEYDOWN:
            keysDown.append(event.key)
         elif event.type == pygame.KEYUP:
            if(event.key in keysDown):
               keysDown.remove(event.key)

      if(K_RETURN in keysDown):
         finished = True
      

      if(K_a in keysDown):
         keysDown.remove(K_a)
         player.glyphs[GLYPH_BULLET_TIME] = (not player.glyphs[GLYPH_BULLET_TIME]) and (glyphsSelected < 3)
         if player.glyphs[GLYPH_BULLET_TIME]: glyphsSelected += 1
         elif (glyphsSelected < 3): glyphsSelected -= 1
      if(K_b in keysDown):
         keysDown.remove(K_b)
         player.glyphs[GLYPH_JUMPER] = not player.glyphs[GLYPH_JUMPER] and (glyphsSelected < 3)
         if player.glyphs[GLYPH_JUMPER]: glyphsSelected += 1
         elif (glyphsSelected < 3): glyphsSelected -= 1
      if(K_c in keysDown):
         keysDown.remove(K_c)
         player.glyphs[GLYPH_DASH] = not player.glyphs[GLYPH_DASH] and (glyphsSelected < 3)
         if player.glyphs[GLYPH_DASH]: glyphsSelected += 1
         elif (glyphsSelected < 3): glyphsSelected -= 1
      if(K_d in keysDown):
         keysDown.remove(K_d)
         player.glyphs[GLYPH_MAGNET] = not player.glyphs[GLYPH_MAGNET] and (glyphsSelected < 3)
         if player.glyphs[GLYPH_MAGNET]: glyphsSelected += 1
         elif (glyphsSelected < 3): glyphsSelected -= 1
      pygame.draw.rect(windowSurface, (0, 0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 0)
      displayTextBox("SECRET DEV SCREEN      " + str(glyphsSelected), (255, 255, 255), 0)
      if(player.glyphs[GLYPH_BULLET_TIME]): colour = (0, 0, 255)
      else: colour = (200, 200, 200) 
      displayTextBox("A                   BULLET TIME ", colour, 1)

      if(player.glyphs[GLYPH_JUMPER]): colour = (0, 0, 255)
      else: colour = (200, 200, 200) 
      displayTextBox("B                   JUMPER ", colour, 2)

      if(player.glyphs[GLYPH_DASH]): colour = (0, 0, 255)
      else: colour = (200, 200, 200) 
      displayTextBox("C                   DASH ", colour, 3)

      if(player.glyphs[GLYPH_MAGNET]): colour = (0, 0, 255)
      else: colour = (200, 200, 200) 
      displayTextBox("D                   MAGNET ", colour, 4)
      
      pygame.display.flip()


pygame.init()
clock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN, 0)
windowSurface.fill((255, 255, 255))
player = Player( windowSurface, spritePlayerWalking, 50, 50, 0, 0, PLAYER_WIDTH, PLAYER_HEIGHT, 50)


while (True):
   devScreen(windowSurface, player)
   playGame(player, 1)

   