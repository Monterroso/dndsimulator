import json
from dndSimulator.GameObjects import createMoveGame

from dndSimulator.Tracker import Tracker

from .context import dndSimulator

from dndSimulator.BoardObjects import simpleBoard


def movementTest():
  tracker = Tracker()
  rounds = 2
  moveGame = createMoveGame(simpleBoard, rounds, tracker)
  moveGame.playGame()

  out_file = open("./output.json", "w")
  
  data = tracker.getSerialized()
  
  json.dump(data, out_file)
  
  out_file.close()