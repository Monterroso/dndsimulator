class PositionObject:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    
  def getNeighborsAtDistance(self, distance=1):
    x = self.x
    y = self.y
    spots = []
    
    spots += [PositionObject(i + x, distance + y) for i in range(-distance, distance + 1)]
    spots += [PositionObject(i + x, -distance + y) for i in range(-distance, distance + 1)]
    
    spots += [PositionObject(distance + x, i + y) for i in range(-distance + 1, distance)]
    spots += [PositionObject(-distance + x, i + y) for i in range(-distance + 1, distance)]
          
    return spots
  
  def distance(self, position):
    pass
  
  def orientation(self, position):
    orientation = ""
    
    if position.x < self.x:
      orientation += "l"
      
    if position.x > self.x:
      orientation += "r"
      
    if position.x != self.x:
      orientation += abs(position.x - self.x)
    
    if position.y < self.y:
      orientation += "d"
      
    if position.y > self.y:
      orientation += "f"
      
    if position.y != self.y:
      orientation += abs(position.y - self.y)
      
    return orientation
      
      