from dndSimulator.Utils import toDict
from .MainAction import MainAction

#Actions taken by entity
class MoveAction(MainAction):
  def __init__(self, mover, destination, start, parent=None, child=None):
    self.mover = mover
    self.destination = destination
    self.start = start
    
    super().__init__(parent=parent, child=child)
    
  def __repr__(self):
    return "{0}: \nEntity: {1}\nStart: {2}\nEnd: {3}".format(self.__class__.__name__, self.mover, self.start, self.destination)

  def attemptDeny(self, denier, game):
    self.deniedBy.append(denier)
    if self.origin.denyAttempt(denier, self, game):
      self.prevented = True
      return True
    
    return False

  def getMover(self):
    return self.mover
  
  def getDestination(self):
    return self.destination

  def perform(self, game):
    game.moveEntity(self.mover, self.destination)

  def getCost(self, game):
      return game.board.getTileAt(self.destination).getCostFrom(self.start - self.destination)
      
  def isValid(self, game):
    if self.mover == self.origin and self.mover.canPayCost(self.getCost(game)):
        return super().isValid(game)
    return False

  def isEntityAction(self):
    return True
  
  def toDict(self, memo, lists):
    return {
      **super().toDict(memo, lists),
      "mover": toDict(self.mover, memo, lists),
      "destination": toDict(self.destination, memo, lists),
      "start": toDict(self.start, memo, lists),
    }