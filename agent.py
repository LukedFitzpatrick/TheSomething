from engineConstants import *
import pygame
import math
from pygame.locals import *
from random import *
from rect import *


class Agent:
   def __init__(self, surface, sprite, x, y, xv, yv, width, height):
      self.sprite = sprite
      self.surface = surface
      self.x = x
      self.y = y
      self.xv = xv
      self.yv = yv
      self.width = width
      self.height = height
      self.jumping = False
      self.targetX = -1
      self.targetY = -1
      self.failureCountdown = 0
      self.uniqueColorR = randrange(0, 255)
      self.uniqueColorG = randrange(0, 255)
      self.uniqueColorB = randrange(0, 255)

   def getRect(self):
      # lol
      selfRect = Rect(int(self.x), int(self.x+self.width), int(self.y), int(self.y+self.height))
      return selfRect

   def moveLeft(self):
      self.xv -= AGENT_XV_INCREMENT

   def moveRight(self):
      self.xv += AGENT_XV_INCREMENT

   def jump(self):
      if not self.jumping:
         self.yv -= AGENT_JUMP_INCREMENT
         self.yv = max(self.yv, -1*MAXIMUM_VELOCITY)
         self.jumping = True


   def handleSituation(self, player):
     
      # the player is within my sight range
      if(math.fabs(player.x - self.x) <= AGENT_LOS and math.fabs(player.y - self.y) <= AGENT_LOS):
         self.targetX = int (player.x + (player.width / 2))
         self.targetY = int (player.y + (player.height / 2))

      # the player isn't within my sight range, I have a target
      elif(self.targetX > 0 and self.targetY > 0):
         if(self.failureCountdown <= 0 or 
            math.fabs(self.x - self.targetX) <= AGENT_LOS and math.fabs(self.y - self.targetY) <= AGENT_LOS):
            self.targetX = randrange(TILE_WIDTH, GAME_SCREEN_WIDTH - TILE_WIDTH)
            self.targetY = randrange(TILE_HEIGHT, GAME_SCREEN_HEIGHT - TILE_HEIGHT)
            # how long I'll keep looking
            self.failureCountdown = AGENT_FAILURE_COUNTDOWN    
      else:
         self.targetX = randrange(TILE_WIDTH, GAME_SCREEN_WIDTH - TILE_WIDTH)
         self.targetY = randrange(TILE_HEIGHT, GAME_SCREEN_HEIGHT - TILE_HEIGHT) 
   
      # move towards the target
      if(self.targetX > self.x):
         self.moveRight()
      if(self.targetX < self.x):
         self.moveLeft()
      if(self.targetY < self.y):
         self.jump()

   def update(self):
      self.x += self.xv
      self.y += self.yv
      self.yv += GRAVITY_INCREMENT
      self.yv = min(self.yv, MAXIMUM_VELOCITY)

      self.failureCountdown -= 1

      if(self.xv > 0):
         self.xv = max(0, self.xv - FRICTION)
      elif(self.xv < 0):
         self.xv = min(0, self.xv + FRICTION)


   def display(self):
      self.sprite.blit(self.surface, (self.x, self.y))
      if BOUNDING_BOX_ON:
         pygame.draw.rect(self.surface, (0, 0, 0) , (self.x,self.y,self.width,self.height), 2)
      if AI_INDICATORS_ON and self.targetX > 0 and self.targetY > 0:
         pygame.draw.line(self.surface, (self.uniqueColorR, self.uniqueColorG, self.uniqueColorB), 
            (self.x, self.y), (self.targetX, self.targetY), 2)
         pygame.draw.circle(self.surface, (self.uniqueColorR, self.uniqueColorG, self.uniqueColorB), 
            (int(self.x+(self.width/2)), int(self.y+self.height/2)), AGENT_LOS, 2)
      if SUBTLE_AI_INDICATORS_ON and self.targetX > 0 and self.targetY > 0:
           pygame.draw.circle(self.surface, (214, 251, 255), 
            (int(self.x+(self.width/2)), int(self.y+self.height/2)), AGENT_LOS, 10)



   def handleCollisions(self, grid):
      # This function is called after the player.update() function.
      # It looks at game grid and moves out of solid blocks.

      # Find which tile we are occupying
      selfyTile = int(self.y/TILE_HEIGHT)
      selfxTile = int((self.x + (self.width/2))/TILE_WIDTH)

      # magic algorithmic code:

      obstacleDistance = self.yv
      if (self.yv > 0): #falling down
         for tile in range(selfyTile+1, NUM_LEVEL_TILES_Y):
            if selfxTile < NUM_LEVEL_TILES_X and tile < NUM_LEVEL_TILES_Y and grid[selfxTile][tile].isSolid:
               distanceToTile = (TILE_HEIGHT*tile) - (self.y + self.height)
               if (distanceToTile < obstacleDistance):
                  obstacleDistance = distanceToTile
                  self.yv *= -PLAYER_BOUNCE_FACTOR
                  self.jumping = False
                  break

      
      elif (self.yv < 0):
         for tile in range(selfyTile, -1, -1):
            if selfxTile < NUM_LEVEL_TILES_X and tile < NUM_LEVEL_TILES_Y and grid[selfxTile][tile].isSolid:
               distanceToTile = (TILE_HEIGHT*(tile+1) - (self.y))
               if (distanceToTile > obstacleDistance):
                  obstacleDistance = (distanceToTile)
                  self.yv  *= -PLAYER_BOUNCE_FACTOR
                  break  

      # we may have moved the selfs y location, so need to recalculate their tile
      selfyTile = int((self.y+obstacleDistance)/TILE_HEIGHT)
      yObs = obstacleDistance
      obstacleDistance = self.xv
      
      if (self.xv > 0):
         for tile in range(selfxTile, NUM_LEVEL_TILES_X):
            if tile < NUM_LEVEL_TILES_X and selfyTile < NUM_LEVEL_TILES_Y and grid[tile][selfyTile].isSolid:
               distanceToTile = (TILE_WIDTH*tile) - (self.x + self.width)
               if (distanceToTile < obstacleDistance):
                  obstacleDistance = distanceToTile
                  self.xv *= -PLAYER_BOUNCE_FACTOR
                  break

      elif (self.xv < 0):
         for tile in range(selfxTile, -1, -1):
            if tile < NUM_LEVEL_TILES_X and selfyTile < NUM_LEVEL_TILES_Y and grid[tile][selfyTile].isSolid:
               distanceToTile = (TILE_WIDTH*(tile+1) - self.x)
               if (distanceToTile > obstacleDistance):
                  obstacleDistance = distanceToTile
                  self.xv *= -PLAYER_BOUNCE_FACTOR
                  break


      self.y += yObs
      self.x += obstacleDistance