from dndsimulator.character.Actions import MoveAction

class AI:
  def __init__(self, boardObject):
    self.boardObject = boardObject
    
  def getAction(self, game):
    #If the execute stack is empty, means it is your turn to act, otherwise you have to react to something else
    pass
  
class RandomMoverAI(AI):
  def getAction(self, game):
    board = self.game.board
    curSpot = self.game.getObjectLocation(self.boardObject)
    
    for cost, spot in board.getSpotsValids(curSpot):
      if cost <= self.boardObject.availableActions["moves"]:
        return MoveAction(self.boardObject, curSpot, spot)
    
    return None