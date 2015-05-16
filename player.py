from engineConstants import *
import pygame

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
      self.jumping = True

   def update(self):
      self.x += self.xv
      self.y += self.yv
      self.yv += GRAVITY_INCREMENT
      self.yv = min(self.yv, MAXIMUM_VELOCITY)

      if(self.xv > 0):
         self.xv = max(0, self.xv - FRICTION)
      elif(self.xv < 0):
         self.xv = min(0, self.xv + FRICTION)



   def handleInput(self, keys):
      if LEFT_KEY in keys:
         self.xv -= PLAYER_XV_INCREMENT
         self.xv = max(self.xv, -1*MAXIMUM_VELOCITY)
      if RIGHT_KEY in keys:
         self.xv += PLAYER_XV_INCREMENT
         self.xv = min(self.xv, MAXIMUM_VELOCITY)
      if JUMP_KEY in keys:
         if not self.jumping:
            self.yv -= JUMP_INCREMENT
            self.yv = max(self.yv, -1*MAXIMUM_VELOCITY)
            self.jumping = True
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
            if grid[selfxTile][tile].isSolid:
               distanceToTile = (TILE_HEIGHT*tile) - (self.y + self.height)
               if (distanceToTile < obstacleDistance):
                  obstacleDistance = distanceToTile
                  self.yv *= -PLAYER_BOUNCE_FACTOR
                  self.jumping = False
                  break

      
      elif (self.yv < 0):
         for tile in range(selfyTile, -1, -1):
            if grid[selfxTile][tile].isSolid:
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
            if grid[tile][selfyTile].isSolid:
               distanceToTile = (TILE_WIDTH*tile) - (self.x + self.width)
               if (distanceToTile < obstacleDistance):
                  obstacleDistance = distanceToTile
                  self.xv *= -PLAYER_BOUNCE_FACTOR
                  break
      
      elif (self.xv < 0):
         for tile in range(selfxTile, -1, -1):
            if grid[tile][selfyTile].isSolid:
               distanceToTile = (TILE_WIDTH*(tile+1) - self.x)
               if (distanceToTile > obstacleDistance):
                  obstacleDistance = distanceToTile
                  self.xv *= -PLAYER_BOUNCE_FACTOR
                  break

      self.y += yObs
      self.x += obstacleDistance
