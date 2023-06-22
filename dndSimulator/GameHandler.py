from .functions.aiGetter import actionFromAI
from .functions.validChecker import isValid
from .functions.perform import perform
from .functions.addToStack import addToStack
from .functions.startTurn import startTurn
from .functions.endTurn import endTurn

class ActionHandler:
  def __init__(self) -> None:
    self.action = None
    
  def getAction(self):
    return self.action
  
  def setAction(self, action):
    self.action = action

  def actionWaiting(self):
    return self.action != None

  def clearAction(self):
    self.action = None

def fixAction(action, backend):
  fixedAction = {}
  
  for key, value in action.items():
    fixedAction[key] = backend.addCompleteObject(value)
    
  return fixedAction

def setAction(action, backend):
  turn = backend.getObj(["currentTurn"])
  actors = backend.getObj(["actors"])
  actorIndex = actors[turn]
  
  backend.setObj(["action"], action, actorIndex)
def isPlayer(ai):
  return ai == "player"

def runUntilBlocked(actionHandler, backend):
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
    
    if not backend.getObj(["isTurn"], actorIndex):
      startTurn(actorIndex, backend)
    
    
    validAction = True
    while validAction == True:
      #Gets the action of the actor, or if player, get from external
      
      if isPlayer(actorAi):
        
        if not actionHandler.actionWaiting():
          return backend.getObj(["id"], actorIndex)
        
        # action = fixAction(actionHandler.getAction(), backend)
        action = actionHandler.getAction()
        setAction(action, backend)
        
        actionHandler.clearAction()
      else: 
        actionIndex = actionFromAI(actorAi, actorIndex, backend)
        action = backend.getObj([], actionIndex)
        setAction(action, backend)
        
      actionIndex = backend.getIndex(["action"], actorIndex)
      
      validAction = isValid(actionIndex, actorIndex, backend)
      
      if validAction:
        addToStack(actionIndex, actorIndex, backend)
        perform(backend)
    
    endTurn(backend)
    