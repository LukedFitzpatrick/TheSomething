import math
from rect import *

class Object:
   def __init__(self, surface, sprite, x, y, timeAlive, wiggle, xv, yv, gravity, width = 32, height = 32):
      self.surface = surface
      self.sprite = sprite
      self.x = x
      self.y = y
      self.xv = xv
      self.yv = yv
      self.gravity = gravity
      self.time = timeAlive
      self.alive = True
      self.wiggle = wiggle
      self.currentWiggle = 0
      self.width = width
      self.height = height

   def updateWiggle(self):
      
      if self.currentWiggle == 0:
         self.currentWiggle += self.wiggle
         self.wiggle *= -1
      if math.fabs(self.currentWiggle) == math.fabs(self.wiggle):
         self.currentWiggle = 0 

   def getRect(self):
      # lol
      selfRect = Rectangle(int(self.x), int(self.x+self.width), int(self.y), int(self.y+self.height))
      return selfRect

   def update(self):
      self.time -= 1
      if(self.time <= 0):
         self.alive = False
      else:
         self.x += self.xv
         self.y += self.yv
         self.yv += self.gravity
         self.updateWiggle()

         self.sprite.blit(self.surface, (self.x+self.wiggle, self.y-self.currentWiggle))
