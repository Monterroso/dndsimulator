from .TupleFactory import createTuple

def ActionMovementFactory(startingPos, endingPos, backend):
  actionTypeIndex = backend.addCompleteObject("move")
  
  startingPosIndex = backend.addCompleteObject(createTuple(startingPos, backend))
  endingPosIndex = backend.addCompleteObject(createTuple(endingPos, backend))
  
  return backend.addCompleteObject({
    "startingPos": startingPosIndex,
    "endingPos": endingPosIndex,
    "actionType": actionTypeIndex
  })