

from Actions import MoveAction


class AI:
  def __init__(self):
    pass
    
  def getAction(self, game, entity):
    #If the execute stack is empty, means it is your turn to act, otherwise you have to react to something else
    pass
  
class RandomMoverAI(AI):
  def getAction(self, game, entity):
    board = game.board
    curSpot = game.getEntityPosition(entity)
    
    for neighbor in board.getNeighborsAt(curSpot):
      offSet = curSpot - neighbor
      cost = board.getTileAt(neighbor).getCostFrom(offSet)
      if entity.canPayCost(cost) and game.isActionStackEmpty():
        return MoveAction(entity, neighbor, curSpot)
    
    return None