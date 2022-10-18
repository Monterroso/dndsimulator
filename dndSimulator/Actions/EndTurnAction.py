from .MainAction import MainAction

class EndTurnAction(MainAction):
  def resolveAction(self, game):
    game.advanceTurn()