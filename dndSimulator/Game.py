from dndSimulator.Actions.MainAction import MainAction
from dndSimulator.Actions.Reaction import Reaction
from dndSimulator.Utils import toDict
from .LogTypes import LogTypes
from .Actions import EndTurnAction, StartTurnAction


class Game:
  def __init__(self, board, entitiesPositions, logger):
    self.board = board
    self.turnOrder = []
    self.entityPositions = {}
    self.actionStack = []
    self.turnNumber = 0
    self.roundCount = 0
    self.logger = logger
    self.actionsTakenStack = []

    for entity, pos in entitiesPositions:
      self.addEntity(entity, pos)

  def isActionStackEmpty(self):
    return len(self.actionStack) == 0
  
  def getNextAction(self):
    if not self.isActionStackEmpty():
      return self.actionStack[0]

  def getEntityActionTakenStack(self, filter):
    return [action for action in self.actionsTakenStack if filter(action)]

  def getCurrentEntityTurn(self):
    return self.turnOrder[self.turnNumber]

  def getTurnsUntilEntityTurn(self, entity):
    (self.turnNumber - self.turnOrder.index(entity)) % len(self.turnOrder)

  def addEntity(self, entity, pos):
    self.turnOrder.append(entity)
    self.turnOrder.sort( key=lambda entity: entity.getInitiative())

    self.entityPositions[entity] = pos

  def getEntityPosition(self, entity):
    return self.entityPositions[entity]

  def moveEntity(self, entity, destination):
    if entity in self.entityPositions:
      self.logger.addLog(LogTypes.ENTITY_MOVED, {"entity": entity, "destination": destination, "origin": self.entityPositions[entity]})
      self.entityPositions[entity] = destination
    else:
      raise Exception("An entity has been attempted to move that is not on the board")

  def addAction(self, action):
    """Adds action to stack, handles cost if origin of action is entity

    Args:
        action (Action): Action to be added to the stack
    """
    self.logger.addLog(LogTypes.ACTION_ADDED, action)
    if action.origin != None:
      cost = action.getCost(self)
      action.origin.payCost(cost)
    self.actionStack.append(action)

  def performAction(self, action):
    self.logger.addLog(LogTypes.ACTION_PERFORMED, action)
    self.actionsTakenStack.append(action)
    self.logger.serialize(self)
    return action.resolveAction(self)
      
  def cycleReactions(self):
    """Cycles through all entities, getting reactions

    Returns:
        bool: Whether or not a reaction was placed onto the stack
    """
    allPassed = True
    for entity in self.turnOrder[::-1]:
        action = entity.getReaction(self)
        if Reaction.isValidAction(action, self):
          self.addAction(action)
          allPassed = False
          
    return allPassed
  
  def buildReactionStack(self):
    """Builds up the stack by cycling through reactions, stopping once all entities pass
    """
    allPassed = False
    while not allPassed:
      allPassed = self.cycleReactions()
  
  def resolveReactionStack(self):
    """Resolves the action stack by building up and resolving the stack, until stack is empty.
    
    Returns if called while stack is empty
    
    One round is performed for reactions if the stack gets emptied, if still empty then exists
    """
    while not self.isActionStackEmpty():
      actionToDo = self.actionStack.pop()
      self.performAction(actionToDo)
      nextAction = actionToDo.getNextAction(self)
      
      if nextAction != None:
        self.addAction(nextAction)
      
      self.buildReactionStack()

  def advanceTurn(self):
    self.turnNumber += 1
    if self.turnNumber == len(self.turnOrder):
      self.turnNumber = 0
      self.roundCount += 1
      self.logger.addLog(LogTypes.ROUND_START)

  def playTurn(self):
    self.addAction(StartTurnAction())
    self.resolveReactionStack()
    
    skippedAction = False
    while not skippedAction:
      entity = self.getCurrentEntityTurn()
      action = entity.getAction(self)
      
      if MainAction.isValidAction(action, self):
        self.addAction(action)
        self.resolveReactionStack()
      else:
        skippedAction = True
      
    self.addAction(EndTurnAction())
    self.resolveReactionStack()

  def checkGameEnd(self):
    return self.roundCount == 2 or len(self.actionsTakenStack) > 100
      

  def playGame(self):
    self.logger.addLog(LogTypes.GAME_START)
    
    while not self.checkGameEnd(): 
      self.playTurn()

    self.logger.addLog(LogTypes.GAME_END)
    
  def toDict(self, memo, lists):
    return {
      "type": type(self).__name__,
      "board": toDict(self.board, memo, lists),
      "turnOrder": toDict(self.turnOrder, memo, lists),
      "entityPositions": toDict(self.entityPositions, memo, lists),
      "actionStack": toDict(self.actionStack, memo, lists),
      "turnNumber": toDict(self.turnNumber, memo, lists),
      "roundCount": toDict(self.roundCount, memo, lists),
      "actionsTakenStack": toDict(self.actionsTakenStack, memo, lists),
    }

    
    

  
