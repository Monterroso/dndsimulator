from ..jsonBackend.factories.ActionFactory import ActionFactory
from ..jsonBackend.factories.TupleFactory import createTuple
from .utils import decompactTupe

def basicMovementAI(actorIndex, actionHandler, backend):
  actorId = backend.getObj(["id"], actorIndex)
  baseStatsIndex = backend.getIndex(["baseStats"], actorIndex)
  
  speed = backend.getObj(["move"], baseStatsIndex)
  position = decompactTupe(backend.getObj(["actorPos", actorIndex]), backend)
  
  newPos = [*position]
  newPos[0] += speed
  
  actionHandler.setAction(actorId, ["move", (newPos,)])

def playerAI(actorIndex, actionHandler, backend):
  pass

def setAction(name, *args, **kwargs):
  if name == "basicMovementAI":
    return basicMovementAI(*args, **kwargs)
  elif name == "player":
    return playerAI(*args, **kwargs)