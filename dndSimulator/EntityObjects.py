from .Entity import Entity
from .StatsObjects import moveStats
from .AIObjects import moveAIObject

def createMoveEntity(log):
    createMoveEntity.count += 1
    return Entity("moveEntity: {0}".format(createMoveEntity.count), [], moveStats, moveAIObject, log )

createMoveEntity.count = -1