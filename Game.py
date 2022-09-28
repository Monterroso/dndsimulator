from LogTypes import LogTypes
from Actions import Action, EndTurnAction, PostAction, StartTurnAction


class Game:
  def __init__(self, board, entitiesPositions, logger):
    self.board = board
    self.turnOrder = []
    self.entityPositions = {}
    self.actionStack = []
    self.turnNumber = 0
    self.roundCount = 0
    self.logger = logger

    for entity, pos in entitiesPositions:
      self.addEntity(entity, pos)

  def isActionStackEmpty(self):
    return len(self.actionStack) == 0

  def getCurrentEntityTurn(self):
    return self.turnOrder[self.turnNumber]

  def addEntity(self, entity, pos):
    self.turnOrder.append(entity)
    self.turnOrder.sort( key=lambda entity: entity.getInitiative())

    self.entityPositions[entity] = pos

  def getEntityPosition(self, entity):
    return self.entityPositions[entity]

  def moveEntity(self, entity, destination):
    if entity in self.entityPositions:
      self.logger.addLog(LogTypes.ENTITY_MOVED, {"entity": entity, "destination": destination})
      self.entityPositions[entity] = destination
    else:
      raise Exception("An entity has been attempted to move that is not on the board")

  def addAction(self, action):
    self.logger.addLog(LogTypes.ACTION_ADDED, action)
    self.actionStack.append(action)

  def performAction(self, action):
    self.logger.addLog(LogTypes.ACTION_PERFORMED, action)
    return action.resolveAction(self)

  def resolveActionStack(self):
    while not self.isActionStackEmpty():
      action = self.actionStack.pop()
      nextAction = self.performAction(action)

    if nextAction is not None:
      self.addAction(nextAction)
      
  def cycleReactions(self):
    allPassed = True
    for entity in self.turnOrder[::-1]:
        action = entity.getReaction(self)
        if issubclass(type(action), Action) and action.isValid(self, entity):
          entity.payCost(action.getBaseCost(self, entity))
          self.addAction(action)
          allPassed = False
          
    return allPassed
  
  def buildReactionStack(self):
    allPassed = False
    while not allPassed:
      allPassed = self.cycleReactions()
  
  def resolveReactionStack(self):
    while len(self.actionStack) >= 1:
      actionToDo = self.actionStack.pop()
      result = self.performAction(actionToDo)
      
      if type(actionToDo) != PostAction:
        self.addAction(PostAction(result))

      self.buildReactionStack()

  def advanceTurn(self):
    self.turnNumber += 1
    if self.turnNumber == len(self.turnOrder):
      self.turnNumber = 0
      self.roundCount += 1

  def playTurn(self):
    self.addAction(StartTurnAction())
    self.buildReactionStack()
    self.resolveReactionStack()
    
    skippedAction = False
    while not skippedAction:
      entity = self.getCurrentEntityTurn()
      action = entity.getAction(self)
      
      if issubclass(type(action), Action) and action.isValid(self, entity):
        self.addAction(action)
        cost = action.getBaseCost(self, entity)
        entity.payCost(cost)
        self.buildReactionStack()
        self.resolveReactionStack()
      else:
        skippedAction = True
      
    self.addAction(EndTurnAction())
    self.buildReactionStack()
    self.resolveReactionStack()

  def checkGameEnd(self):
    return self.roundCount == 2
      

  def playGame(self):
    self.logger.addLog(LogTypes.GAME_START, self.roundCount)
    
    while not self.checkGameEnd(): 
      self.playTurn()

    self.logger.addLog(LogTypes.GAME_END, self.roundCount)

    
    

  
