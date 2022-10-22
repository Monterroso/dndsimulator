from dndSimulator.Utils import toDict
from .Cost import Cost


class Tile:
  def __init__(self, neighborMoveData, height=0):
    self.height = height
    self.neighborMoveData = neighborMoveData
    
  def __repr__(self):
    return "Tile: Height: {0}, neighbors: {1}".format(self.height, self.neighborMoveData)

  def getHeight(self):
    return self.height

  def getNeighbors(self):
    return [neighbor for neighbor in self.neighborMoveData]
  
  def getCostFrom(self, position):
    if position in self.neighborMoveData:
      return self.neighborMoveData[position]
    
    return Cost(isInfinite=True)
  
  def toDict(self, memo, lists):
    return {
      "type": type(self).__name__,
      "height": toDict(self.height, memo, lists),
      "neighborMoveData": toDict(self.neighborMoveData, memo, lists),
    }
  