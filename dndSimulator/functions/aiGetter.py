from ..jsonBackend.factories.ActionFactory import ActionMovementFactory
from ..jsonBackend.factories.TupleFactory import createTuple
from .utils import decompactTupe

def basicMovementAI(actorIndex, backend):
  baseStatsIndex = backend.getIndex(["baseStats"], actorIndex)
  
  speed = backend.getObj(["move"], baseStatsIndex)
  position = decompactTupe(backend.getObj(["actorPos", actorIndex]), backend)
  
  newPos = [*position]
  newPos[0] += speed
  
  return ActionMovementFactory(position, newPos, backend)

def playerAI(actorIndex, backend):
  return backend.getObj(["action"], actorIndex)

def actionFromAI(name, *args, **kwargs):
  if name == "basicMovementAI":
    return basicMovementAI(*args, **kwargs)
  elif name == "player":
    return playerAI(*args, **kwargs)