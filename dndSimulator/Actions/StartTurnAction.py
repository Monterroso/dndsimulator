from .MainAction import MainAction
from dndSimulator.LogTypes import LogTypes
from dndSimulator.Cost import Cost

#Actions to be used by the game for dictating turns
class StartTurnAction(MainAction):
  def perform(self, game, tracker):
    oldActions = self.origin.startTurn()
    tracker.addAction(LogTypes.START_TURN, {"Action": self, "OldActions": oldActions, "NewActions": self.origin.getAvailableActions()})
    
  def undoPerform(self, game, tracker):
    super().undoPerform(game, tracker)
    game.getCurrentEntityTurn().undoStartTurn(self.oldActions)