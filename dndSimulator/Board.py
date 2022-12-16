from .Cost import Cost

class Board:
  """Board object, with position: tile pairs, and various methods for traversal across
  """
  def __init__(self, positionTileList):
    self.tiles = {}
    for pos, tile in positionTileList:
      self.tiles[pos] = tile
      
  def getTileAt(self, position):
    """Gets tile at given position

    Args:
        position (Position): Position to get tile from

    Returns:
        Tile: tile at specified position
    """
    return self.tiles[position]
    
  def getNeighborsAt(self, position):
    """Gets the positions of all the neighbors at the given position

    Args:
        position (Position): origin to get neighbors from

    Returns:
        Position[]: List of all the positions that are neighbors
    """
    return [position + neighbor for neighbor in self.getTileAt(position).getNeighbors()]

  # def getPathCost(self, positionList):
  #   """Gets the created cost following the path provided

  #   Args:
  #       positionList (Position[]): List of positions to be traversed

  #   Returns:
  #       Cost: created cost following the path
  #   """
  #   prevCost = Cost()

  #   for i in range(1, len(positionList)):
  #     prevPos = positionList[i - 1]
  #     curPos = positionList[i]
  #     prevCost += self.tiles[curPos].getCostFrom(prevPos - curPos)
    
  #   return prevCost
  
  def toDict(self, serializer):
    return {
      "tiles": serializer(self.tiles)
    }