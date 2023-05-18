def perform(backend):
  actionStack = backend.getObj(["actionStack"])
  
  actorIndex, actionIndex = backend.getObj([], actionStack[-1])
  
  actionType = backend.getObj(["actionType"], actionIndex)
  
  if actionType == "move":
    endingPosIndex = backend.getIndex(["endingPos"], actionIndex)
    
    actorDict = backend.getObj(["actorPos"])
    
    newActorDict = {**actorDict}
    newActorDict[actorIndex] = endingPosIndex
    
    #Updates the position of the actor
    backend.setObj(["actorPos"], newActorDict)
    
  newActionStack = actionStack[:-1]
  
  #Removes the action from the list
  backend.setObj(["actionStack"], newActionStack)
  
  #Sets change block
  backend.endChangeBlock()