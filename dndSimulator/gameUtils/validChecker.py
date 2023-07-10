from .getCost import getCost
from .utils import decompactTupe

def isValid(actionIndex, actorIndex, backend):
  availableActionsIndex = backend.getIndex(["availableActions"], actorIndex)
  availableActions = backend.getObj(["availableActions"], actorIndex)
  
  if backend.getObj(["actionType"], actionIndex) == "move":
    endingPos = backend.getObj(["proposedAction", "endingPos"])
    dims = decompactTupe(backend.getObj(["board", "dims"]), backend)

    for index, pos in enumerate(decompactTupe(endingPos, backend)):
      if pos > dims[index]:
        return False

  costIndex = getCost(actionIndex, actorIndex, backend)

  costObj = backend.getFromWorkingIndex(costIndex)
  
  isEmpty = True

  for costType in costObj:
    if costType not in availableActions:
      return False
    
    availableAmount = backend.getObj([costType], availableActionsIndex)
    neededAmount = backend.getObj([costType], costIndex)
    
    if neededAmount > 0:
      isEmpty = False
    
    diff = availableAmount - neededAmount
    
    if diff < 0:
      return False
    
  return not isEmpty
    
    