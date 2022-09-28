from Game import Game

from BoardObjects import simpleBoard
from Logger import Logger
from EntityObjects import createMoveEntity
from PositionObjects import EmptyPosition


def simpleTest():
    log = Logger()

    testGame = Game(simpleBoard, [(createMoveEntity(log), EmptyPosition,)], log)

    testGame.playGame()

    log.printLog()