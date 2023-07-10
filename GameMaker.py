from .dndSimulator.Engine import Engine
from .dndSimulator.gameFactories import GameFactory
from .dndSimulator.gameUtils import gameRotation
from .dndSimulator.ActionHandler import ActionHandler

class SimpleMovementGame:
  def __init__(self, actorDatas, actorTypeDatas, board):
    """Inputs used to create a game handler

    Args:
        actorDatas (list): [actorName (string), actorType (string), ai (string)]
        actorTypeDatas (list): [actorType (string), speed (int)]
        board (list): [dims (list<int>)]
    """

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

    GameFactory.createGame(actors, actorTypes, board, self.backend)

  def setAction(self, actorId, actionData):
    self.handler.setAction(actorId, actionData)

  def run(self):
    return gameRotation(self.handler, self.backend)

  def serialize(self):
    return {
      "handler": self.handler.serialize(),
      "backend": self.backend.serialize(),
    }