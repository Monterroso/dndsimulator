from .Engine import Engine
from .gameFactories import createGame
from .gameUtils import gameRotation
from .ActionHandler import ActionHandler

class SimpleMovementGame:
  def __init__(self, actorDatas=None, actorTypeDatas=None, board=None, data=None):
    """Inputs used to create a game handler

    Args:
        actorDatas (list): [actorName (string), actorType (string), ai (string)]
        actorTypeDatas (list): [actorType (string), speed (int)]
        board (list): [dims (list<int>)]
        gameJson (dict): game in json form 
    """

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

  def setAction(self, actorId, actionData):
    self.handler.setAction(actorId, actionData)

  def run(self):
    return gameRotation(self.handler, self.backend)

  def serialize(self):
    return {
      "handler": self.handler.serialize(),
      "backend": self.backend.serialize(),
    }