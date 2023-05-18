import dndSimulator.jsonBackend.factories.GameFactory as GameFactory

from dndSimulator.jsonBackend.Backend import Backend

from dndSimulator.RunGame import basicActionGame

import json

def nameTest():
  backend = Backend()
  
  actorDatas = [
    ["actor1", "speed1", "basicMovementAI"],
    ["actor2", "speed2", "basicMovementAI"],
    ["actor3", "speed3", "basicMovementAI"],
  ]
  
  actors = []
  
  for actorData in actorDatas:
    name, actorType, ai = actorData
    actors.append({"name": name, "baseStats": actorType, "ai": ai})
      
  actorTypeDatas = [
    ["speed1", 1],
    ["speed2", 2],
    ["speed3", 3],
  ]
  
  actorTypes = []
  for actorTypeData in actorTypeDatas:
    name, speed = actorTypeData
    actorTypes.append({"name": name, "move": speed})
      
  board = {"dims": (5, 5,)}

  GameFactory.createGame(actors, actorTypes, board, backend)

  print(basicActionGame(backend))
  print(basicActionGame(backend))
  print(basicActionGame(backend))
  print(basicActionGame(backend))
  print(basicActionGame(backend))
  print(basicActionGame(backend))
  
  
  
def temp():
  
  backend = Backend()

  first = backend.createEmpty()

  #Got the index of the first, now create the others
  a = backend.addCompleteObject({"value": 1})
  b = backend.addCompleteObject({"value": 2})
  backend.addCompleteObject({"a": a, "b": b})
  ab = backend.addCompleteObject({"a": a, "b": b})

  backend.completeEmpty(first, {"a": a, "b": b, "ab": ab, "H": first})

  backend.setObj(["H"], {"value": 2})
  backend.setObj(["D"], {"value": 2})
  backend.setObj(["D"], {"value": 3})

  backend.endChangeBlock()

  backend.remove(["D"])
  backend.setObj(["D"], {"value": 2})
  d = backend.addCompleteObject({"value": 4})
  c = backend.addCompleteObject({"value": 3})

  backend.setObj(["ab",  "a"], {"value": 3})
  
  backend.endChangeBlock()
  backend.remove(["D"])

  e = backend.addCompleteObject({"value": 5})
  f = backend.addCompleteObject({"value": 6})
  
  backend.endChangeBlock()
  
  w = open("newFormat.json", "w+")
  w.write(json.dumps(backend.changes))
