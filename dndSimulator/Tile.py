from .Cost import Cost


class Tile:
  def __init__(self, neighborMoveData, height=0):
    self.height = height
    self.neighborMoveData = neighborMoveData

  def getHeight(self):
    return self.height

  def getNeighbors(self):
    return [neighbor for neighbor in self.neighborMoveData]
  
  def getCostFrom(self, position):
    if position in self.neighborMoveData:
      return self.neighborMoveData[position]
    
    return Cost(isInfinite=True)
  