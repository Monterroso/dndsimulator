from dndSimulator.Actions import MoveAction, Reaction
from dndSimulator.LogTypes import LogTypes

class PreventOverlapMove(Reaction):
  def __init__(self, toDeny, child=None, parent=None):
    self.toDeny = toDeny
    
    super().__init__(parent=parent, child=child)
    
  def isValid(self, game):
    if MoveAction.isAction(self.toDeny):
      if self.toDeny.getDestination() == game.getEntityPosition(self.getOrigin()):
        if not self.toDeny.hasAttemptedDeny(self.getOrigin()):
          return True

    return False
  
  def perform(self, game, tracker):
    success = self.toDeny.attemptDeny(self.origin, game)
    tracker.addAction(LogTypes.ACTION_PREVENTED, {"Action": self, "Success": success, "Denier": self.origin, "ToDeny": self.toDeny})
    
  def undoPerform(self, game, tracker):
    super().undoPerform(game, tracker)
    self.toDeny.undoAttemptDeny(self.origin, game)
    
  def toDict(self, serializer):
    return {
      **super().toDict(serializer),
      "toDeny": serializer(self.toDeny),
    }