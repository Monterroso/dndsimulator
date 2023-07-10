from .getCost import getCost

def addToStack(actionIndex, actorIndex, backend):
  availableActionsIndex = backend.getIndex(["availableActions"], actorIndex)
  
  costIndex = getCost(actionIndex, actorIndex, backend)

  costObj = backend.getFromWorkingIndex(costIndex)
  availableActions = backend.getFromWorkingIndex(availableActionsIndex)
  
  newAvailableActions = {}

  #Gets intersection of the keys
  for costType in costObj.keys() & availableActions.keys():
    

    availableAmount = backend.getObj([costType], availableActionsIndex)
    neededAmount = backend.getObj([costType], costIndex)
    
    diffIndex = backend.addCompleteObject(availableAmount - neededAmount)

    newAvailableActions[costType] = diffIndex
    
  #Subtracts the cost of the action from the actor performing action
  backend.setObj(["availableActions"], newAvailableActions, actorIndex)
  
  newActionStack = [*backend.getObj(["actionStack"])]
  
  actionInfoIndex = backend.addCompleteObject((actorIndex, actionIndex,))
  
  newActionStack.append(actionInfoIndex)
  
  #Updates the action stack to include the new action
  backend.setObj(["actionStack"], tuple(newActionStack))

  backend.endChangeBlock()