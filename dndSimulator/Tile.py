from .Serializer import objectSerializer
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
  
  def serialize(self, serializer):
    serializer.startObject(None, self.__repr__())
    serializer.addProperty("height", self.height)
    neighborObj = {}
    for pos, cost in self.neighborMoveData.items():
      posJSON = objectSerializer.serialize(pos)
      costJSON = objectSerializer.serialize(cost)
      
      neighborObj[repr(pos)] = [posJSON, costJSON]
      
    serializer.addProperty("neighborMoveData", neighborObj)
  