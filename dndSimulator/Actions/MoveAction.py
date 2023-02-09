from .MainAction import MainAction
from dndSimulator.LogTypes import LogTypes

#Actions taken by entity
class MoveAction(MainAction):
  def __init__(self, mover, destination, start, parent=None, child=None):
    self.mover = mover
    self.destination = destination
    self.start = start
    
    super().__init__(origin=mover, parent=parent, child=child)
    
  def __repr__(self):
    return "{0}: \nEntity: {1}\nStart: {2}\nEnd: {3}".format(self.__class__.__name__, self.mover, self.start, self.destination)

  def denyLogic(self, denier, game):
    return self.origin.attemptDeny(denier, self, game)

  def getMover(self):
    return self.mover
  
  def getDestination(self):
    return self.destination

  def perform(self, game, tracker):
    game.moveEntity(self.mover, self.destination)
    tracker.addAction(LogTypes.ENTITY_MOVED, {"Action": self, "Mover": self.mover, "Destination": self.destination, "Start": self.start})
    
  def undoPerform(self, game, tracker):
    super().undoPerform(game, tracker)
    game.moveEntity(self.mover, self.origin)

  def getCost(self, game):
    return game.getCostFrom(self.start, self.destination, self.mover)
      
  def isValid(self, game):
    if self.mover == self.origin and self.mover.canPayCost(self.getCost(game)):
      return super().isValid(game)
    return False

  def isEntityAction(self):
    return True
  
  def toDict(self, serializer):
    return {
      **super().toDict(serializer),
      "mover": serializer(self.mover),
      "destination": serializer(self.destination),
      "start": serializer(self.start),
    }