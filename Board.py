class Board:
  def __init__(self, positionTileList):
    self.tiles = {}
    for pos, tile in positionTileList:
      self.tiles[pos] = tile
      
  def getTileAt(self, position):
    return self.tiles[position]
  
  def getNeighborsAtDistance(self, position, distance=1):
    return [pos for pos in position.getNeighborsAtDistance(distance) if pos in self.tiles]
  
  def tileConverter(self, origin, dest):
    pass
    
  def getPathCosts(self, positionList):
    
    if len(positionList) < 2:
      return 0
    
    prevPos = self.getTileAt(position[0])
    
    
    for position in positionList[1:]:
      self.getTileAt(prevPos).getCostDirectionTo(prevPos.orientation(position))