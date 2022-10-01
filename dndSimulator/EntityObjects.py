from .Entity import Entity
from .StatsObjects import moveStats
from .AIObjects import moveAIObject

def createMoveEntity(log):
    return Entity([], moveStats, moveAIObject, log )