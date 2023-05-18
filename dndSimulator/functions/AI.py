from ..jsonBackend.factories.ActionFactory import ActionMovementFactory

def basicMovementAI(actorIndex, backend):
  baseStatsIndex = backend.getIndex(["baseStats"], actorIndex)
  
  speed = backend.getObj(["move"], baseStatsIndex)
  position = backend.getObj(["actorPos", actorIndex])
  
  newPos = [*position,]
  newPos[0] += speed
  
  return ActionMovementFactory(position, newPos, backend)

def functions(name, *args, **kwargs):
  if name == "basicMovementAI":
    return basicMovementAI(*args, **kwargs)