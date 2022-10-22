import json

from dndSimulator.Utils import toDict
from .context import dndSimulator

from dndSimulator.Game import Game
from dndSimulator.BoardObjects import simpleBoard
from dndSimulator.Logger import Logger
from dndSimulator.EntityObjects import entityFactory
from dndSimulator.PositionObjects import OriginPosition
from dndSimulator.LogTypes import LogTypes
from dndSimulator.Actions import PostAction


def simpleTest():
    log = Logger()

    testGame = Game(simpleBoard, [(entityFactory.createMoveEntity(), OriginPosition,), (entityFactory.createGhostMoveEntity(), OriginPosition,)], log)

    testGame.playGame()
    
    def filter(action):
        return action.isEntityAction() and not issubclass(PostAction, type(action))

    out_file = open("./text.json", "w")
    
    json.dump(log.getSerialized(), out_file)
    
    # out_file.close()
    
    # print(testGame.getEntityActionTakenStack(filter))

    logs = log.getLog(filter=[LogTypes.ENTITY_MOVED],
                 dataFilter=[PostAction])
    
    positionMap = {}
    
    for log in logs:
        _, data = log
        entity = data["entity"]
        destination = data["destination"]
        origin = data["origin"]
        
        if entity not in positionMap:
            positionMap[entity] = [origin]
            
        positionMap[entity].append(destination)
        
    print(positionMap)
    
    