from .MainAction import MainAction
from dndSimulator.LogTypes import LogTypes

class EndTurnAction(MainAction):
  def perform(self, game, tracker):
    oldTurnInfo = game.advanceTurn()
    tracker.addAction(LogTypes.END_TURN, {"Action": self, "NewTurn": game.turnNumber(), "NewRound": game.getRoundCount(), **oldTurnInfo})
    
  def undoPerform(self, game, tracker):
    super().undoPerform(game, tracker)
    game.reverseTurn()