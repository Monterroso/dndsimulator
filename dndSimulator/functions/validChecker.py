from .getCost import getCost

def isValid(actionIndex, actorIndex, backend):
  availableActionsIndex = backend.getIndex(["availableActions"], actorIndex)
  availableActions = backend.getObj(["availableActions"], actorIndex)
  
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
    
    