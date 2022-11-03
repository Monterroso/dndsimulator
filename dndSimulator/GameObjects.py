import json
from dndSimulator.EndConditions.EndAfterXRounds import EndAfterXRounds

from dndSimulator.Game import Game
from dndSimulator.BoardObjects import twoTileBoard
from dndSimulator.EntityObjects import entityFactory
from dndSimulator.PositionObjects import OriginPosition


def createMoveGame(rounds, log):
  winCons = [EndAfterXRounds(rounds)]
  return Game(twoTileBoard, [(entityFactory.createMoveEntity(0), OriginPosition,), (entityFactory.createMoveEntity(1), OriginPosition,), (entityFactory.createGhostMoveEntity(2), OriginPosition,)], winCons, log)
