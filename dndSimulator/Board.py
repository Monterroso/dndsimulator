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
  
  def toDict(self, serializer):
    return {
      "tiles": serializer(self.tiles)
    }