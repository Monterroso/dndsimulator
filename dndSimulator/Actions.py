from .Cost import Cost
from .Results import Result

class TopAction:
  pass

class MainAction(TopAction):
  pass

class Reaction(TopAction):
  pass

class Action:
  def __init__(self):
    self.result = None

  def getBaseCost(self, game, origin):
    return Cost()

  def resolveAction(self, game):
    self.result = Result(self, {})
  
  def getNextAction(self, game, origin):
    return PostAction(self,self.result)

  def isValid(self, game, origin):
    return True

class PostAction(Action):
  def __init__(self, result):
    self.result = result
  
class StartTurnAction(Action):
  def resolveAction(self, game):
    game.getCurrentEntityTurn().startTurn()
    return super().resolveAction(game)
  
  
class EndTurnAction(Action):
  def resolveAction(self, game):
    game.advanceTurn()
    return super().resolveAction(game)

  def isValid(self, game, origin):
    return game.getCurrentEntityTurn() == origin and game.isActionStackEmpty()
  
class MoveAction(Action):
  def __init__(self, mover, destination, start):
    self.mover = mover
    self.destination = destination
    self.start = start

  def resolveAction(self, game):
    game.moveEntity(self.mover, self.destination)
    print(game.entityPositions)
    return super().resolveAction(game)

  def getBaseCost(self, game, origin):
      return game.board.getTileAt(self.destination).getCostFrom(self.start - self.destination)
      
  def isValid(self, game, origin):
    if self.mover == origin and game.isActionStackEmpty() and \
      self.mover.canPayCost(self.getBaseCost(game, origin)):
        return True
    return False