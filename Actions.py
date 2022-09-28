from Cost import Cost


class Action:
  def __init__(self):
    pass

  def getBaseCost(self, game, origin):
    return Cost()

  def resolveAction(self, game):
    return PostAction(self) 

  def isValid(self, origin):
    return True

class PreAction(Action):
  def __init__(self, action):
    self.action = action

  def resolveAction(self, game):
    return self.action

class PostAction(Action):
  def __init__(self, action):
    self.action = action

  def resolveAction(self):
    return None

class EndTurnAction(Action):
  def resolveAction(self, game):
    game.advanceTurn()

  def isValid(self, game, origin):
    return game.getCurrentEntityTurn() == origin
  
class MoveAction(Action):
  def __init__(self, mover, destination, start):
    self.mover = mover
    self.destination = destination
    self.start = start

  def resolveAction(self, game):
    game.moveEntity(self.mover, self.destination)
    return super().resolveAction(game)

  def getBaseCost(self, game, origin):
      return game.board.getTileAt(self.destination).getCostFrom(self.start - self.destination)
      
  def isValid(self, game, origin):
    if self.mover == origin and game.isActionStackEmpty() and \
      self.mover.canPayCost(self.getBaseCost(game, origin)):
        return True
    return False

class MultiAttackAction(Action):
  def __init__(self, attacker, attacks):
    self.attacker = attacker,
    self.attacks = attacks