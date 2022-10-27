from dndSimulator.Actions import MoveAction

def getAction(game, entity):
  board = game.board
  curSpot = game.getEntityPosition(entity)
  
  moves = []
  
  for neighbor in board.getNeighborsAt(curSpot):
    offSet = curSpot - neighbor
    cost = board.getTileAt(neighbor).getCostFrom(offSet)
    if entity.canPayCost(cost) and game.isActionStackEmpty():
      moves.append(MoveAction(entity, neighbor, curSpot))
  
  if len(moves) != 0:
    return moves[-1]