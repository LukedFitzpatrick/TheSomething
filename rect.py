def range_overlap(a_min, a_max, b_min, b_max):
    '''Neither range is completely greater than the other
    '''
    overlapping = True
    if (a_min > b_max) or (a_max < b_min):
        overlapping = False
    return overlapping

class Rectangle:
   def __init__(self, left, right, top, bottom):
      self.left = left
      self.right = right
      self.top = top
      self.bottom = bottom

   def collides(self, r2):
      return (range_overlap(self.left, self.right, r2.left, r2.right) and 
      range_overlap(self.top, self.bottom, r2.top, r2.bottom))
