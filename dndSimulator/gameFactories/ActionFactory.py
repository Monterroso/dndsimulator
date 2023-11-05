from .TupleFactory import createTuple
    
def moveAction(actionTypeIndex, data, backend):
  endingPosIndex = backend.addCompleteObject(createTuple(data[0], backend))
    
  return backend.addCompleteObject({
    "endingPos": endingPosIndex,
    "actionType": actionTypeIndex
  })
  
def noneAction(actionTypeIndex, data, backend):
  return backend.addCompleteObject({"actionType": actionTypeIndex})


class ActionCreator:
  def __init__(self, actionTypes=None):
    self.actionTypes = actionTypes if actionTypes == None else {}
    
  def addActionCreator(self, key, actionFunction):
    self.actionTypes[key] = actionFunction
    
  def __call__(self, actionType, data, backend):
    actionTypeIndex = backend.addCompleteObject(actionType)
    
    return self.actionTypes[actionType](actionTypeIndex, data, backend)


createAction = ActionCreator()
createAction.addActionCreator("none", noneAction)
createAction.addActionCreator("move", moveAction)