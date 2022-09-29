from Game import Game

from BoardObjects import simpleBoard
from LogTypes import LogTypes
from Logger import Logger
from EntityObjects import createMoveEntity
from PositionObjects import EmptyPosition


def simpleTest():
    log = Logger()

    testGame = Game(simpleBoard, [(createMoveEntity(log), EmptyPosition,)], log)

    testGame.playGame()
    filter = [LogTypes.ROUND_START, LogTypes.GAME_START, LogTypes.GAME_END, LogTypes.ENTITY_MOVED]
    log.printLog(filter)