import json
from dndSimulator.Serializer.Serializer import objectSerializer
from .context import dndSimulator

from dndSimulator.Game import Game
from dndSimulator.BoardObjects import simpleBoard
from dndSimulator.Logger import Logger
from dndSimulator.EntityObjects import createMoveEntity
from dndSimulator.PositionObjects import EmptyPosition
from dndSimulator.LogTypes import LogTypes
from dndSimulator.Actions import PostAction


def simpleTest():
    log = Logger()

    testGame = Game(simpleBoard, [(createMoveEntity(log), EmptyPosition,)], log)

    testGame.playGame()
    
    def filter(action):
        return action.isEntityAction() and not PostAction.isValidAction(action, testGame)
    
    serialed = objectSerializer.serialize(testGame)
    
    out_file = open("./text.json", "w")

    obj = json.loads(serialed)
    
    json.dump(obj, out_file)
    
    out_file.close()
    
    # print(testGame.getEntityActionTakenStack(filter))

    # log.printLog(filter=[LogTypes.ROUND_START, LogTypes.ACTION_PERFORMED, LogTypes.GAME_START, LogTypes.GAME_END, LogTypes.ENTITY_MOVED],
    #              dataFilter=[PostAction])