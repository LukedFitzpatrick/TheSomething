from engineConstants import *
import pygame
from rect import *
import math
from graphics import *

class Player:
   def __init__(self, surface, sprite, x, y, xv, yv, width, height, rage):
      self.sprite = sprite
      self.surface = surface
      self.x = x
      self.y = y
      self.xv = xv
      self.yv = yv
      self.width = width
      self.height = height
      self.rage = rage
      self.jumping = 1
      self.collisionBlock = COLLISION_BLOCK
      self.justChangedDirection = False
      self.charging = False
      self.chargeCounter = -1
      self.leftDoubleCounter = 100
      self.rightDoubleCounter = 100

   def annoy(self):
      self.rage = min(100, self.rage + RAGE_INCREMENT)
      self.collisionBlock = COLLISION_BLOCK

   def getRect(self):
      # lol
      selfRect = Rectangle(int(self.x), int(self.x+self.width), int(self.y), int(self.y+self.height))
      return selfRect

   def closeTo(self, other):
      if(math.fabs(self.x - other.x) <= CLOSENESS_TRIGGER and math.fabs(self.y - other.y) <= CLOSENESS_TRIGGER):
         return True
      else:
         return False

   def chargeKill(self):
      self.rage += CHARGE_KILL_ANGER_INCREMENT

   def fireKill(self):
      self.rage += FIRE_KILL_ANGER_INCREMENT

   def nukeKill(self):
      self.rage += NUKE_KILL_ANGER_INCREMENT

   def update(self):
      self.x += self.xv
      self.y += self.yv
      self.yv += GRAVITY_INCREMENT
      self.yv = min(self.yv, MAXIMUM_VELOCITY)
      self.collisionBlock = max(0, self.collisionBlock - 1)

      self.rage = max(0, self.rage - RAGE_DECREMENT)

      if(self.chargeCounter > 0):
         self.chargeCounter -= 1
      if(self.chargeCounter == 0):
         self.xv = 0
         self.charging = False
         self.sprite = spritePlayerWalking
         self.chargeCounter = -1

      if(self.xv > 0):
         self.xv = max(0, self.xv - FRICTION)
      elif(self.xv < 0):
         self.xv = min(0, self.xv + FRICTION)

   def armourKill(self):
      self.rage += ARMOUR_KILL_RAGE_INCREMENT

   def infectionKill(self):
      self.rage += INFECTION_KILL_RAGE_INCREMENT

   def handleKeyUp(self, key):
      if key == LEFT_KEY:
         self.leftDoubleCounter = 0
      if key == RIGHT_KEY:
         self.rightDoubleCounter = 0


   def charge(self):
      self.charging = True
      self.chargeCounter = CHARGE_DURATION
      self.sprite = spriteChargingPlayer

   def handleInput(self, keys):
      if LEFT_KEY in keys:
         if self.leftDoubleCounter < DOUBLE_TAP_FRAMES and (GLYPH_DASH or GLYPH_CHARGE):
            self.xv -= PLAYER_XV_DASH_INCREMENT
            if(GLYPH_CHARGE):
               self.charge()
         else:
            self.xv -= PLAYER_XV_INCREMENT
            self.xv = max(self.xv, -1*MAXIMUM_VELOCITY)
      else:
         self.leftDoubleCounter += 1
      
      if RIGHT_KEY in keys:
         if self.rightDoubleCounter < DOUBLE_TAP_FRAMES and (GLYPH_DASH or GLYPH_CHARGE):
            self.xv += PLAYER_XV_DASH_INCREMENT
            if(GLYPH_CHARGE):
               self.charge()
         else:   
            self.xv += PLAYER_XV_INCREMENT
            self.xv = min(self.xv, MAXIMUM_VELOCITY)
      else:
         self.rightDoubleCounter += 1


      if DOWN_KEY in keys:
         self.yv += PLAYER_XV_INCREMENT

      if JUMP_KEY in keys:
         if self.jumping == 0 or (GLYPH_JUMPER and self.jumping == 1):
            if self.jumping == 0:
               self.yv -= JUMP_INCREMENT
            else:
               self.yv -= DOUBLE_JUMP_INCREMENT
            self.yv = max(self.yv, -1*MAXIMUM_VELOCITY)
            self.jumping += 1
            keys.remove(JUMP_KEY)
     
      return keys
   
   def display(self):
      self.sprite.blit(self.surface, (self.x, self.y))
      if BOUNDING_BOX_ON:
         pygame.draw.rect(self.surface, (0, 0, 0) , (self.x,self.y,self.width,self.height), 2)


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
            if tile < NUM_LEVEL_TILES_Y and selfxTile < NUM_LEVEL_TILES_X and grid[selfxTile][tile].isSolid:
               distanceToTile = (TILE_HEIGHT*tile) - (self.y + self.height)
               if (distanceToTile < obstacleDistance):
                  obstacleDistance = distanceToTile
                  self.yv *= -PLAYER_BOUNCE_FACTOR
                  self.jumping = 0
                  break

      
      elif (self.yv < 0):
         for tile in range(selfyTile, -1, -1):
            if tile < NUM_LEVEL_TILES_Y and selfxTile < NUM_LEVEL_TILES_X and grid[selfxTile][tile].isSolid:
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
            if grid[tile][selfyTile].isSolid and tile < NUM_LEVEL_TILES_X and selfyTile < NUM_LEVEL_TILES_Y:
               distanceToTile = (TILE_WIDTH*tile) - (self.x + self.width)
               if (distanceToTile < obstacleDistance):
                  obstacleDistance = distanceToTile
                  self.xv *= -PLAYER_BOUNCE_FACTOR
                  if GLYPH_JUMPER:
                     self.jumping = 0
                  break
      
      elif (self.xv < 0):
         for tile in range(selfxTile, -1, -1):
            if grid[tile][selfyTile].isSolid and tile < NUM_LEVEL_TILES_X and selfyTile < NUM_LEVEL_TILES_Y:
               distanceToTile = (TILE_WIDTH*(tile+1) - self.x)
               if (distanceToTile > obstacleDistance):
                  obstacleDistance = distanceToTile
                  self.xv *= -PLAYER_BOUNCE_FACTOR
                  if GLYPH_JUMPER:
                     self.jumping = 0
                  break

      self.y += yObs
      self.x += obstacleDistance
