from ..Serializer import objectSerializer
from .MainAction import MainAction

#Actions taken by entity
class MoveAction(MainAction):
  def __init__(self, mover, destination, start):
    self.mover = mover
    self.destination = destination
    self.start = start
    
    super().__init__()
    
  def __repr__(self):
    return "{0}: \nEntity: {1}\nStart: {2}\nEnd: {3}".format(self.__class__.__name__, self.mover, self.start, self.destination)

  def resolveAction(self, game):
    game.moveEntity(self.mover, self.destination)

  def getCost(self, game):
      return game.board.getTileAt(self.destination).getCostFrom(self.start - self.destination)
      
  def isValid(self, game):
    if self.mover == self.origin and self.mover.canPayCost(self.getCost(game)):
        return super().isValid(game)
    return False

  def isEntityAction(self):
    return True
  
  def serialize(self, serializer):
    serializer.startObject(None, repr(self))
    serializer.addProperty("mover", objectSerializer.serialize(self.mover))
    serializer.addProperty("destination", objectSerializer.serialize(self.destination))
    serializer.addProperty("start", objectSerializer.serialize(self.start))