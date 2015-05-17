import random
class Trace:
   def __init__(self, surface, darkness, death, increment, x, y):
      self.darkness = darkness
      self.increment = increment
      self.death = death
      self.surface = surface
      self.alive = True
      self.x = int(x)
      self.y = int(y)

   def update(self):
      self.display()
      self.darkness += self.increment

      if self.darkness > self.death:
         self.alive = False



   def display(self):
      for x in range(random.choice([self.x-2, self.x-1, self.x]), self.x+2):
         for y in range(self.y-1,self.y+2):
            self.surface.set_at((x, y), (self.darkness, self.darkness, 0))