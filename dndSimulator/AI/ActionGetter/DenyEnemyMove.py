from dndSimulator.Actions import MoveAction
from dndSimulator.Actions.PreventOverlapMove import PreventOverlapMove

class DenyEnemyMove:
  def __call__(self, game, entity):
    nextAction = game.getNextAction()
    if MoveAction.isValidAction(nextAction, game) \
        and nextAction.getMover().getTeam() != entity.getTeam() \
        and nextAction.getDestination() == game.getEntityPosition(entity) \
        and not nextAction.isDenier(entity):
      return PreventOverlapMove(nextAction)
      
denyEnemyMove = DenyEnemyMove()