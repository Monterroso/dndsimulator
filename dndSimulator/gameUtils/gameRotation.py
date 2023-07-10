from dndSimulator.gameFactories import createAction
from .aiGetter import setAction
from .validChecker import isValid
from .perform import perform
from .addToStack import addToStack
from .startTurn import startTurn
from .endTurn import endTurn

def gameRotation(actionHandler, backend):
  """This function takes a backend json, and runs action cycle.\
    Actor gives an action, if valid performs. If invalid, increments turn counter
  
  Args:
      backend (Backend): backend to be run for a cycle

  Returns:
      int: team victor, -1 if no victor
  """
  
  while True:
  
    #Gets the current actor of the turn
    turn = backend.getObj(["currentTurn"])
    actors = backend.getObj(["actors"])
    actorIndex = actors[turn]
    actorAi = backend.getObj(["ai"], actorIndex)
    actorId = backend.getObj(["id"], actorIndex)
    
    if not backend.getObj(["turnStarted"]):
      startTurn(actorIndex, backend)
    
    validAction = True
    while validAction == True:
      #Gets the action of the actor, or if player, get from external
      setAction(actorAi, actorIndex, actionHandler, backend)

      if actionHandler.canSkip(actorId):
        return actorId

      actionIndex = createAction(*actionHandler.popAction(actorId), backend)
      backend.setIndex(["proposedAction"], actionIndex)

      validAction = isValid(actionIndex, actorIndex, backend)
      
      if validAction: 
        addToStack(actionIndex, actorIndex, backend)
        perform(backend)

      #Action is no longer proposed
      backend.setObj(["proposedAction"], None)
    
    endTurn(backend)
    