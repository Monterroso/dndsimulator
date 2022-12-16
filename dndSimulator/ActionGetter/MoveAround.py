from dndSimulator.Actions import MoveAction

def getAction(game, entity):
  """Moves around the board

  Args:
      Game (Game): current game
      Entity (Entity): entity the ai is attached to

  Returns:
      Action: Move action if any are available
  """
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