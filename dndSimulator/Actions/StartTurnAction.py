from .MainAction import MainAction

#Actions to be used by the game for dictating turns
class StartTurnAction(MainAction):
  def perform(self, game):
    game.getCurrentEntityTurn().startTurn()