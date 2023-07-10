from .TupleFactory import createTuple

def createAction(actionType, data, backend):
  actionTypeIndex = backend.addCompleteObject(actionType)

  if actionType == "none":
    return backend.addCompleteObject({"actionType": actionTypeIndex})

  if actionType == "move":
    endingPosIndex = backend.addCompleteObject(createTuple(data[0], backend))
    
    return backend.addCompleteObject({
      "endingPos": endingPosIndex,
      "actionType": actionTypeIndex
    })
  