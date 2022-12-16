import json
from dndSimulator.EndConditions.EndAfterXRounds import EndAfterXRounds

from dndSimulator.Game import Game
from dndSimulator.EntityObjects import entityFactory
from dndSimulator.PositionObjects import OriginPosition

def createGame(entities, board, rounds, log):
  winCons = [EndAfterXRounds(rounds)]
  return Game(board, entities, winCons, log)

def createMoveGame(board, rounds, log):
  return createGame([ \
    (entityFactory.createMoveEntity(0), OriginPosition,), \
    (entityFactory.createMoveEntity(1), OriginPosition,), \
    (entityFactory.createGhostMoveEntity(2), OriginPosition,) \
    ], board, rounds, log)
  
def createGuidedMoveGame(board, rounds, log):
  return createGame([ \
    (entityFactory.createMoveEntity(0), OriginPosition,), \
    (entityFactory.createMoveEntity(1), OriginPosition,), \
    (entityFactory.createMoveEntity(2), OriginPosition,) \
    ], board, rounds, log)
