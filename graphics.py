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

spriteInfectedAgent = pyganim.PygAnimation([('graphics/tempInfectedAgent.png', 1)])
spriteInfectedAgent.play()


spriteAnnoy = pyganim.PygAnimation([('graphics/annoyed.png', 1)])
spriteAnnoy.play()

spriteParticle = pyganim.PygAnimation([('graphics/redPixel.png', 1)])
spriteParticle.play()

spriteMagnet = pyganim.PygAnimation([('graphics/magnet.png', 1)])
spriteMagnet.play()

spriteFire = pyganim.PygAnimation([('graphics/fire.png', 1)])
spriteFire.play()

spriteVoid = pyganim.PygAnimation([('graphics/void.png', 1)])
spriteVoid.play()

spriteSmokescreenPlayer = pyganim.PygAnimation([('graphics/smokescreenPlayer.png', 1)])
spriteSmokescreenPlayer.play()

spriteChargingPlayer = pyganim.PygAnimation([('graphics/tempChargingPlayer.png', 1)])
spriteChargingPlayer.play()

#glyphs

spriteJumperGlyph = pyganim.PygAnimation([('graphics/jumperGlyph.png', 1)])
spriteJumperGlyph.play()

spriteBulletTimeGlyph = pyganim.PygAnimation([('graphics/bulletTimeGlyph.png', 1)]) 
spriteJumperGlyph = pyganim.PygAnimation([('graphics/jumperGlyph.png', 1)])
spriteDashGlyph = pyganim.PygAnimation([('graphics/dashGlyph.png', 1)]) 
spriteMagnetGlyph = pyganim.PygAnimation([('graphics/magnetGlyph.png', 1)])
spriteSmokescreenGlyph = pyganim.PygAnimation([('graphics/smokescreenGlyph.png', 1)])
spriteArmourGlyph = pyganim.PygAnimation([('graphics/armourGlyph.png', 1)])
spriteInfectionGlyph = pyganim.PygAnimation([('graphics/infectionGlyph.png', 1)])
spriteChargeGlyph = pyganim.PygAnimation([('graphics/chargeGlyph.png', 1)])
spriteFireGlyph = pyganim.PygAnimation([('graphics/fireGlyph.png', 1)])
spriteNukeGlyph = pyganim.PygAnimation([('graphics/nukeGlyph.png', 1)])
spriteVoidGlyph = pyganim.PygAnimation([('graphics/voidGlyph.png', 1)])
spriteEmptyGlyph = pyganim.PygAnimation([('graphics/emptyGlyph.png', 1)])

spriteEmptyGlyph.play()
spriteBulletTimeGlyph.play()
spriteJumperGlyph.play()
spriteDashGlyph.play()
spriteMagnetGlyph.play()
spriteSmokescreenGlyph.play()
spriteArmourGlyph.play()
spriteInfectionGlyph.play()
spriteChargeGlyph.play()
spriteFireGlyph.play()
spriteNukeGlyph.play()
spriteVoidGlyph.play()


genericSolid = pygame.image.load('graphics/genericSolid.png')
blankSpace = pygame.image.load('graphics/blankSpace.png')


def makeAnnoySymbol(surface, player, objects):
   tempObject = Object(surface, spriteAnnoy, player.x+15, player.y-32, 15, 1, 0, 0, 0.1)
   objects.append(tempObject)
   return objects


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