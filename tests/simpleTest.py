import json

from .context import dndSimulator

from dndSimulator.Game import Game
from dndSimulator.BoardObjects import simpleBoard
from dndSimulator.Logger import Logger
from dndSimulator.EntityObjects import entityFactory
from dndSimulator.PositionObjects import OriginPosition
from dndSimulator.LogTypes import LogTypes


def simpleTest():
  log = Logger()
  testGame = Game(simpleBoard, [(entityFactory.createMoveEntity(), OriginPosition,), (entityFactory.createGhostMoveEntity(), OriginPosition,)], log)

  testGame.playGame()

  out_file = open("./display/public/data/text.json", "w")
  
  json.dump(log.getSerialized(), out_file)
  
  # out_file.close()

  logs = log.getLog(filter=[LogTypes.ENTITY_MOVED], dataFilter=[])
  
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
    
    