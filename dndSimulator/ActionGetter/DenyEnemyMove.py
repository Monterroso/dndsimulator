from dndSimulator.Actions import MoveAction
from dndSimulator.Actions.PreventOverlapMove import PreventOverlapMove

class DenyEnemyMove:
  """Attempts to prevent other entities not on the same team
  """
  def __call__(self, game, entity):
    """Attempts to prevent other entities not on the same team

      Args:
          Game (Game): current game
          Entity (Entity): entity the ai is attached to

      Returns:
          Action: Deny move action or none
      """
    nextAction = game.getNextAction()
    if MoveAction.isAction(nextAction) \
        and nextAction.getMover().getTeam() != entity.getTeam() \
        and nextAction.getDestination() == game.getEntityPosition(entity) \
        and not nextAction.isDenier(entity):
      return PreventOverlapMove(nextAction)
      
denyEnemyMove = DenyEnemyMove()