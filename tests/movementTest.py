import json
from dndSimulator.GameObjects import createMoveGame

from dndSimulator.LoggerObjects import createLogger

from .context import dndSimulator

from dndSimulator.Game import Game
from dndSimulator.BoardObjects import simpleBoard
from dndSimulator.Logger import Logger
from dndSimulator.EntityObjects import entityFactory
from dndSimulator.PositionObjects import OriginPosition
from dndSimulator.LogTypes import LogTypes
from dndSimulator.Actions import PostAction


def moveTest():
  log = createLogger()
  rounds = 2
  moveGame = createMoveGame(rounds, log)
  moveGame.playGame()

  out_file = open("./output.json", "w")
  
  data = log.getSerialized()
  
  json.dump(data, out_file)
  
  out_file.close()