from dndSimulator.Actions import MoveAction, Reaction

class PreventOverlapMove(Reaction):
  def __init__(self, toDeny, child=None, parent=None):
    self.toDeny = toDeny
    
    super().__init__(parent=parent, child=child)
    
  def isValid(self, game):
    if MoveAction.isAction(self.toDeny):
      if self.toDeny.getDestination() == game.getEntityPosition(self.getOrigin()):
        if not self.isDenier(self.toDeny.getOrigin()):
          return True

    return False
  
  def perform(self, game):
    self.toDeny.attemptDeny(self, game)
    
  def toDict(self, serializer):
    return {
      **super().toDict(serializer),
      "toDeny": serializer(self.toDeny),
    }