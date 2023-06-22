from .utils import getDistance, decompactTupe

def getCost(actionIndex, actorIndex, backend):
  actionType = backend.getObj(["actionType"], actionIndex)
  
  cost = {}
  
  if actionType == "move":
    startingPos = backend.getObj(["startingPos"], actionIndex)
    endingPos = backend.getObj(["endingPos"], actionIndex)
    
    moveAmount = getDistance(decompactTupe(startingPos, backend), decompactTupe(endingPos, backend))
    moveAmountIndex = backend.addCompleteObject(moveAmount)
    
    cost["move"] = moveAmountIndex
    
  
  return backend.addCompleteObject(cost)
    
    