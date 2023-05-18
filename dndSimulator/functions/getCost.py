from .utils import getDistance

def getCost(actionIndex, actorIndex, backend):
  actionType = backend.getObj(["actionType"], actionIndex)
  
  cost = {}
  
  if actionType == "move":
    startingPos = backend.getObj(["startingPos"], actionIndex)
    endingPos = backend.getObj(["endingPos"], actionIndex)
    
    moveAmount = getDistance(startingPos, endingPos)
    moveAmountIndex = backend.addCompleteObject(moveAmount)
    
    cost["move"] = moveAmountIndex
    
  
  return backend.addCompleteObject(cost)
    
    