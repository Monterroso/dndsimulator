from .MainAction import MainAction

class EndTurnAction(MainAction):
  def perform(self, game):
    game.advanceTurn()