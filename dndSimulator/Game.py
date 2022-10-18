from dndSimulator.Actions.MainAction import MainAction
from dndSimulator.Actions.Reaction import Reaction
from .Serializer import objectSerializer
from .LogTypes import LogTypes
from .Actions import Action, EndTurnAction, PostAction, StartTurnAction


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
    self.logger.addLog(LogTypes.ACTION_ADDED, action)
    self.actionStack.append(action)

  def performAction(self, action):
    self.logger.addLog(LogTypes.ACTION_PERFORMED, action)
    self.actionsTakenStack.append(action)
    return action.resolveAction(self)
      
  def cycleReactions(self):
    allPassed = True
    for entity in self.turnOrder[::-1]:
        action = entity.getReaction(self)
        if Reaction.isValidAction(action, self):
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
      self.performAction(actionToDo)
      nextAction = actionToDo.getNextAction(self)
      
      if nextAction != None:
        self.addAction(nextAction)
        
      self.buildReactionStack()

  def handleReactionStack(self):
    self.buildReactionStack()
    self.resolveReactionStack()

  def advanceTurn(self):
    self.turnNumber += 1
    if self.turnNumber == len(self.turnOrder):
      self.turnNumber = 0
      self.roundCount += 1
      self.logger.addLog(LogTypes.ROUND_START)

  def playTurn(self):
    self.addAction(StartTurnAction())
    self.handleReactionStack()
    
    skippedAction = False
    while not skippedAction:
      entity = self.getCurrentEntityTurn()
      action = entity.getAction(self)
      
      if MainAction.isValidAction(action, self):
        self.addAction(action)
        cost = action.getCost(self)
        entity.payCost(cost)
        self.handleReactionStack()
      else:
        skippedAction = True
      
    self.addAction(EndTurnAction())
    self.handleReactionStack()

  def checkGameEnd(self):
    return self.roundCount == 2 or len(self.actionsTakenStack) > 100
      

  def playGame(self):
    self.logger.addLog(LogTypes.GAME_START)
    
    while not self.checkGameEnd(): 
      self.playTurn()

    self.logger.addLog(LogTypes.GAME_END)
    
  def serialize(self, serializer):
    serializer.startObject(None, repr(self))
    
    serializer.addProperty("board", objectSerializer.serialize(self.board))
    serializer.addProperty("turnOrder", [objectSerializer.serialize(entity) for entity in self.turnOrder])
    
    entPosObj = {}
    for pos, entity in self.entityPositions.items():
      entPosObj[repr(pos)] = [objectSerializer.serialize(pos), objectSerializer.serialize(entity)]
      
    serializer.addProperty("entityPositions", entPosObj)
    serializer.addProperty("actionStack", [objectSerializer.serialize(action) for action in self.actionStack])
    serializer.addProperty("turnNumber", self.turnNumber)
    serializer.addProperty("roundCount", self.roundCount)
    serializer.addProperty("logger", objectSerializer.serialize(self.logger))
    serializer.addProperty("actionsTakenStack", [objectSerializer.serialize(action) for action in self.actionsTakenStack])

    
    

  
