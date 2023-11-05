from .utils import getDistance, decompactTupe

def getCost(actionIndex, actorIndex, backend):
  """Gets the cost of the action, stores 

  Args:
      actionIndex (_type_): _description_
      actorIndex (_type_): _description_
      backend (_type_): _description_

  Returns:
      _type_: _description_
  """
  actionType = backend.getObj(["actionType"], actionIndex)
  
  cost = {}
  
  if actionType == "move":
    startingPos = backend.getObj(["actorPos", actorIndex])
    endingPos = backend.getObj(["endingPos"], actionIndex)
    
    moveAmount = getDistance(decompactTupe(startingPos, backend), decompactTupe(endingPos, backend))
    moveAmountIndex = backend.addCompleteObject(moveAmount)
    
    cost["move"] = moveAmountIndex
    
  
  return backend.addCompleteObject(cost)