from .jsonBackend.Backend import createPrimitive
from .functions.AI import functions
from .functions.validChecker import isValid
from .functions.perform import perform
from .functions.addToStack import addToStack
from .functions.startTurn import startTurn
def runGame(backend):
  """Takes a backend, and runs a single turn

  Args:
      backend (Backend): data of the game
  """
  
  turn = backend.getObj(["currentTurn"])
  
  actors = backend.getObj(["actors"])
  
  backend.setObj(["currentTurn"], (turn + 1) % len(actors))
  
  backend.endChangeBlock()


def basicActionGame(backend):
  """This function takes a backend json, and runs action cycle.\
    Actor gives an action, if valid performs. If invalid, increments turn counter
  
  Args:
      backend (Backend): backend to be run for a cycle

  Returns:
      int: team victor, -1 if no victor
  """
  
  #Gets the current actor of the turn
  turn = backend.getObj(["currentTurn"])
  actors = backend.getObj(["actors"])
  actorIndex = actors[turn]
  actorAi = backend.getObj(["ai"], actorIndex)
  
  
  validAction = True
  while validAction == True:
    #Gets the action of the actor
    actionIndex = functions(actorAi, actorIndex, backend)
    
    validAction = isValid(actionIndex, actorIndex, backend)
    
    if validAction:
      addToStack(actionIndex, actorIndex, backend)
      perform(backend)
  
  #Increments turn once current turn is done
  newTurnNumber = (turn + 1) % len(actors)
  backend.setObj(["currentTurn"], newTurnNumber)
  backend.endChangeBlock()
  
  startTurn(actors[newTurnNumber], backend)
  
  
  #Return status code if turn is done
  return -1