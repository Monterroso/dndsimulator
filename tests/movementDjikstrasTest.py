import json
from dndSimulator.GameObjects import createMoveGame

from dndSimulator.LoggerObjects import createLogger

from .context import dndSimulator

from dndSimulator.BoardObjects import mediumBoard


def movementTest():
  log = createLogger()
  rounds = 2
  moveGame = createMoveGame(mediumBoard, rounds, log)
  moveGame.playGame()

  out_file = open("./output.json", "w")
  
  data = log.getSerialized()
  
  json.dump(data, out_file)
  
  out_file.close()