from .context import dndSimulator

from dndSimulator.Game import Game
from dndSimulator.BoardObjects import simpleBoard
from dndSimulator.Logger import Logger
from dndSimulator.EntityObjects import createMoveEntity
from dndSimulator.PositionObjects import EmptyPosition


def simpleTest():
    log = Logger()

    testGame = Game(simpleBoard, [(createMoveEntity(log), EmptyPosition,)], log)

    testGame.playGame()