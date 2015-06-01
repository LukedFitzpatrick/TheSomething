from graphics import *
from pygame.locals import *
class Glyph:
   def __init__(self, sprite, name, unlocked, available, active, selectionKey):
      self.sprite = sprite
      self.name = name
      self.unlocked = unlocked
      self.available = available
      self.active = active
      self.selectionKey = selectionKey
      self.availableColour = (0, 0, 255)
      self.notAvailableColour = (200, 200, 255) 

   def getTextColour(self):
      if(self.available):
         return self.availableColour
      else:
         return self.notAvailableColour

bulletTimeGlyph = Glyph(spriteBulletTimeGlyph, "A   Bullet Time", True, False, False, K_a)
jumperGlyph = Glyph(spriteJumperGlyph, "B   Double Jump", True, False, False, K_b) 
dashGlyph = Glyph(spriteDashGlyph, "C   Dash", True, False, False, K_c)
magnetGlyph = Glyph(spriteMagnetGlyph, "D   Magnet", True, False, False, K_d)
smokescreenGlyph = Glyph(spriteSmokescreenGlyph, "E   Smokescreen", True, False, False, K_e)
armourGlyph = Glyph(spriteArmourGlyph, "F   Armour", True, False, False, K_f)
infectionGlyph = Glyph(spriteInfectionGlyph, "G   Infection", True, False, False, K_g)
chargeGlyph = Glyph(spriteChargeGlyph, "H   Charge", True, False, False, K_h)
fireGlyph = Glyph(spriteFireGlyph, "I   Fire", True, False, False, K_i)
nukeGlyph = Glyph(spriteNukeGlyph, "J   Nuke", True, False, False, K_j)
voidGlyph = Glyph(spriteVoidGlyph, "K   Void", True, False, False, K_k)
emptyGlyph = Glyph(spriteEmptyGlyph, "L   Empty", True, False, False, K_l)