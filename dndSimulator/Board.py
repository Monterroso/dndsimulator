from dndSimulator.Serializer import Serializer, objectSerializer
from .Cost import Cost

class Board:
  def __init__(self, positionTileList):
    self.tiles = {}
    for pos, tile in positionTileList:
      self.tiles[pos] = tile
      
  def getTileAt(self, position):
    return self.tiles[position]
    
  def getNeighborsAt(self, position):
    return [position + neighbor for neighbor in self.getTileAt(position).getNeighbors()]

  def getPathCost(self, positionList):
    prevCost = Cost()

    for i in range(1, len(positionList)):
      prevPos = positionList[i - 1]
      curPos = positionList[i]
      prevCost += self.tiles[curPos].getCostFrom(prevPos - curPos)
    
    return prevCost
  
  def serialize(self, serializer):
    serializer.startObject(None, "Board")
    
    tileObj = {}
    for pos, tile in self.tiles.items():
      posJSON = objectSerializer.serialize(pos)
      tileJSON = objectSerializer.serialize(tile)
      
      tileObj[repr(pos)] = [posJSON, tileJSON]
      
    serializer.addProperty("tiles", tileObj)