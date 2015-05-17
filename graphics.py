import pygame
from pygame.locals import *
import pyganim
from object import *
import random
from random import *


# create the PygAnimation objects
spritePlayerWalking = pyganim.PygAnimation([('graphics/tempPlayer.png', 1)])
spritePlayerWalking.play()

spriteGenericAgent = pyganim.PygAnimation([('graphics/tempAgent.png', 1)])
spriteGenericAgent.play()

spriteAnnoy = pyganim.PygAnimation([('graphics/annoyed.png', 1)])
spriteAnnoy.play()

spriteParticle = pyganim.PygAnimation([('graphics/redPixel.png', 1)])
spriteParticle.play()

genericSolid = pygame.image.load('graphics/genericSolid.png')
blankSpace = pygame.image.load('graphics/blankSpace.png')

def particlePuff(surface, sprite, density, x, y, objects, direction):
   if direction < 0:
      bottom = -10
      top = -1
   elif direction > 0:
      bottom = 1
      top = 10
   else:
      bottom = -1
      top = 1

   for i in range(0, density):
      particle = Object(surface, sprite, x, y, 10, 0, randrange(bottom, top), -4, 1)
      objects.append(particle)
   
   return objects