from .Entity import Entity
from .StatsObjects import moveStats, ghostMoveStats
from .AI.AIObjects import moveAIObject


class EntityFactory:
  def __init__(self):
    self.entity = -1

  def createMoveEntity(self, team):
    self.entity += 1
    return Entity("{0} moveEntity".format(self.entity), [], moveStats, moveAIObject, team)

  def createGhostMoveEntity(self, team):
      self.entity += 1
      return Entity("{0} ghostMoveEntity".format(self.entity), [], ghostMoveStats, moveAIObject, team)


entityFactory = EntityFactory()