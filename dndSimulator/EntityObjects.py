from .Entity import Entity
from .StatsObjects import moveStats, ghostMoveStats
from .Object.AI.AIObjects import moveAIObject


class EntityFactory:
    def __init__(self):
        self.entity = -1

    def createMoveEntity(self):
        self.entity += 1
        return Entity("{0} moveEntity".format(self.entity), [], moveStats, moveAIObject, 0)

    def createGhostMoveEntity(self):
        self.entity += 1
        return Entity("{0} ghostMoveEntity".format(self.entity), [], ghostMoveStats, moveAIObject, 0)


entityFactory = EntityFactory()