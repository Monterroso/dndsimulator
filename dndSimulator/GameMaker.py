from dndSimulator.Engine import Engine
from dndSimulator.gameFactories import createGame
from dndSimulator.gameUtils import gameRotation, getCurrentTurnId
from dndSimulator.ActionHandler import ActionHandler
from dndSimulator.gameUtils.utils import getHash

class SimpleMovementGame:
  def __init__(self, actorDatas=None, actorTypeDatas=None, board=None, data=None):
    """Inputs used to create a game handler

    Args:
        actorDatas (list): [actorName (string), actorType (string), ai (string)]
        actorTypeDatas (list): [actorType (string), speed (int)]
        board (list): [dims (list<int>)]
        gameJson (dict): game in json form 
    """

    actorDatas = actorDatas if actorDatas != None else []
    actorTypeDatas = actorTypeDatas if actorTypeDatas != None else []
    board = board if board != None else [(5,5,)]

    if data != None:
      gameData = data["backend"]
      handlerData = data["handler"]

      self.backend = Engine(data=gameData)
      self.handler = ActionHandler(handlerData)
    else:
      self.backend = Engine()
    
      actors = []
      for actorData in actorDatas:
        name, actorType, ai = actorData
        actors.append({"name": name, "baseStats": actorType, "ai": ai})
      
      actorTypes = []
      for actorTypeData in actorTypeDatas:
        name, speed = actorTypeData
        actorTypes.append({"name": name, "move": speed})
          
      board = {"dims": board[0]}
      
      self.handler = ActionHandler()

      createGame(actors, actorTypes, board, self.backend)

  def getNextActor(self):
    return getCurrentTurnId(self.backend)

  def setAction(self, actorId, actionData):
    self.handler.setAction(actorId, actionData)

  def run(self):
    return gameRotation(self.handler, self.backend)

  def serialize(self):
    return {
      "handler": self.handler.serialize(),
      "backend": self.backend.serialize(),
    }

  def getHash(self):
    return getHash(self.serialize["backend"])