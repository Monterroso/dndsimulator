from dndSimulator.Actions import MoveAction
from dndSimulator.Item import Item
from dndSimulator.Utils import djkistras

cookie = Item("Cookie")

class MoveToCookie:
  def __init__(self):
    self.path = []
    
  def __call__(self, game, entity):
    """Moves to get the cookie on the board

    Args:
        Game (Game): current game
        Entity (Entity): entity the ai is attached to

    Returns:
        Action: Move action if any are available to get closer
    """
    curSpot = game.getEntityPosition(entity)
    
    if len(self.path) != 0:
      cost = game.getCostFrom(curSpot, self.path[0], entity)
      if entity.canPayCost(cost):
        dest = self.path[0]
        self.path = self.path[1:]
        return MoveAction(entity, dest)
    else:
      self.path = djkistras(curSpot, game.getItem)