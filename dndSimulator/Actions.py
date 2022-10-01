from .Cost import Cost
from .Results import Result

#Base for all actions
class Action:
  def __init__(self):
    self.result = None

  def getCost(self, game, origin):
    return Cost()

  def resolveAction(self, game):
    self.result = Result(self, {})
  
  def getNextAction(self, game, origin):
    return None

  def isValid(self, game, origin):
    return False

  def onPrevent(self, game, origin):
    if origin is not None:
      origin.payCost(-self.getCost(game, origin))

  def isEntityAction(self):
    return False


  @classmethod
  def isValid(cls, action, game, origin):
    return issubclass(type(action), cls) and action.isValid(game, origin)


#Base action types
class MainAction(Action):
  def getNextAction(self, game, origin):
    return PostAction(self)

  def isValid(self, game, origin):
    return game.isActionStackEmpty()

class Reaction(Action):
  def getNextAction(self, game, origin):
    return PostAction(self)

class PostAction(Action):
  def __init__(self, action):
    self.action = action

#Actions to be used by the game for dictating turns
class StartTurnAction(MainAction):
  def resolveAction(self, game):
    game.getCurrentEntityTurn().startTurn()
  
class EndTurnAction(MainAction):
  def resolveAction(self, game):
    game.advanceTurn()

#Actions taken by entity
class MoveAction(MainAction):
  def __init__(self, mover, destination, start):
    self.mover = mover
    self.destination = destination
    self.start = start

  def resolveAction(self, game):
    game.moveEntity(self.mover, self.destination)

  def getCost(self, game, origin):
      return game.board.getTileAt(self.destination).getCostFrom(self.start - self.destination)
      
  def isValid(self, game, origin):
    if self.mover == origin and self.mover.canPayCost(self.getCost(game, origin)):
        return super().isValid(game, origin)
    return False

  def isEntityAction(self):
    return True