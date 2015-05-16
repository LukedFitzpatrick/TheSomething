import pygame
from pygame.locals import *
import pyganim


# create the PygAnimation objects
spritePlayerWalking = pyganim.PygAnimation([('graphics/tempPlayer.png', 1)])
spritePlayerWalking.play()

spriteGenericAgent = pyganim.PygAnimation([('graphics/tempAgent.png', 1)])
spriteGenericAgent.play()

genericSolid = pygame.image.load('graphics/genericSolid.png')
blankSpace = pygame.image.load('graphics/blankSpace.png')