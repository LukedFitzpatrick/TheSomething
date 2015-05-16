import pygame
from pygame.locals import *
import pyganim


# create the PygAnimation objects
spritePlayerWalking = pyganim.PygAnimation([('graphics/tempPlayer.png', 1)])
spritePlayerWalkingFlip = pyganim.PygAnimation([('graphics/tempPlayer.png', 1)])

spritePlayerWalking.rate = 4
spritePlayerWalkingFlip.rate = 4

spritePlayerWalking.play()
spritePlayerWalkingFlip.play()


genericSolid = pygame.image.load('graphics/genericSolid.png')
blankSpace = pygame.image.load('graphics/blankSpace.png')