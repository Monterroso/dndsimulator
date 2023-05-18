def ActionMovementFactory(startingPos, endingPos, backend):
  actionTypeIndex = backend.addCompleteObject("move")
  
  startingPosIndex = backend.addCompleteObject(startingPos)
  endingPosIndex = backend.addCompleteObject(endingPos)
  
  return backend.addCompleteObject({
    "startingPos": startingPosIndex,
    "endingPos": endingPosIndex,
    "actionType": actionTypeIndex
  })