from dndSimulator.Actions.MainAction import MainAction
from dndSimulator.Actions.Reaction import Reaction
from dndSimulator.Stats import Skills
from .LogTypes import LogTypes
from .Actions import EndTurnAction, StartTurnAction


class Game:
  def __init__(self, board, entitiesPositions, endCons, tracker):
    self.board = board
    self.turnOrder = []
    self.entityPositions = {}
    self.actionStack = []
    self.turnNumber = 0
    self.roundCount = 0
    self.endCons = endCons
    self.tracker = tracker
    self.actionsTakenStack = []
    self.itemPositions = {}
    
    tracker.addObject(self)

    for entity, pos in entitiesPositions:
      self.addEntity(entity, pos)

  def isActionStackEmpty(self):
    return len(self.actionStack) == 0
  
  def getRoundCount(self):
    return self.roundCount
  
  def getNextAction(self):
    if not self.isActionStackEmpty():
      return self.actionStack[-1]
    
  def getCostFrom(self, origin, destination, entity):
    destinationTile = self.board.getTileAt(destination)
    fromPosition = destination - origin
    
    baseCost = destinationTile.getCostFrom(self, fromPosition)
    
    return baseCost

  def getEntityActionTakenStack(self, filter):
    return [action for action in self.actionsTakenStack if filter(action)]

  def getCurrentEntityTurn(self):
    return self.turnOrder[self.turnNumber]

  def getTurnsUntilEntityTurn(self, entity):
    (self.turnNumber - self.turnOrder.index(entity)) % len(self.turnOrder)

  def addEntity(self, entity, pos, ghost=False):
    
    if not ghost:
      self.tracker.addAction(LogTypes.ENTITY_ADDED, {entity, pos})

    self.turnOrder.append(entity)
    self.turnOrder.sort( key=lambda entity: entity.getSkill(Skills.Initiative))

    self.entityPositions[entity] = pos
    
  def addItem(self, item, pos, ghost=False):
    
    if not ghost:
      self.tracker.addAction(LogTypes.ITEM_ADDED, {item, pos})

    self.itemPositions[item] = pos
    
  def removeEntity(self, entity, ghost=False):
    
    if not ghost:
      self.tracker.addAction(LogTypes.ENTITY_REMOVED, {entity})
    
    self.turnOrder.remove(entity)
    self.turnOrder.sort( key=lambda entity: entity.getSkill(Skills.Initiative))
    
    del self.entityPositions[entity]

  def removeItem(self, item, ghost=False):
    
    if not ghost:
      self.tracker.addAction(LogTypes.ITEM_REMOVED, {item})
    
    del self.itemPositions[item]

  def getEntityPosition(self, entity):
    return self.entityPositions[entity]
  
  def getItemPosition(self, item):
    return self.itemPositions[item]
  
  def getEntitiesAt(self, position):
    entities = []
    for eposition, entity in self.entityPositions.items():
      if position == eposition:
        entities.append(entity)
    
    return entities
  
  def getItemsAt(self, position):
    items = []
    for eposition, item in self.itemPositions.items():
      if position == eposition:
        items.append(item)
        
    return items

  def moveEntity(self, entity, destination, ghost=False):
    
    if not ghost:
      self.tracker.addAction(LogTypes.ENTITY_MOVED, {entity, destination})
    
    self.entityPositions[entity] = destination
    
  def moveItem(self, item, destination, ghost=False):
    
    if not ghost:
      self.tracker.addAction(LogTypes.ITEM_MOVED, {item, destination})
    
    self.itemPositions[item] = destination

  def addAction(self, action, ghost=False):
    """Adds action to stack, handles cost if origin of action is entity

    Args:
        action (Action): Action to be added to the stack
    """
    
    if not ghost:
      self.tracker.addAction(LogTypes.ACTION_ADDED, {action})
      
    action.onAdd(self)
    self.actionStack.append(action)

  def performAction(self, action, ghost=False):
    
    if not ghost:
      self.tracker.addAction(LogTypes.ACTION_PERFORMED, {action})
      
    self.actionsTakenStack.append(action)
    self.tracker.serialize(self)
    action.resolveAction(self)
      
  def cycleReactions(self):
    """Cycles through all entities, getting reactions

    Returns:
        bool: Whether or not a reaction was placed onto the stack
    """
    allPassed = True
    for entity in self.turnOrder[:-1]:
      action = entity.getReaction(self)
      if Reaction.isAction(action) and action.isValid(self):
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
      self.buildReactionStack()
      
      actionToDo = self.actionStack.pop()
      self.performAction(actionToDo)
      
  def advanceTurn(self):
    self.turnNumber += 1
    if self.turnNumber == len(self.turnOrder):
      self.turnNumber = 0
      self.roundCount += 1
      self.tracker.addLog(LogTypes.ROUND_START)

  def playTurn(self):
    self.addAction(StartTurnAction(self))
    self.resolveReactionStack()
    
    skippedAction = False
    while not skippedAction:
      entity = self.getCurrentEntityTurn()
      action = entity.getAction(self)
      
      if MainAction.isAction(action) and action.isValid(self):
        self.addAction(action)
        self.resolveReactionStack()
      else:
        skippedAction = True
      
    self.addAction(EndTurnAction(self))
    self.resolveReactionStack()

  def checkGameEnd(self):
    for endCon in self.endCons:
      if endCon(self) == True:
        return True
      
    return False
      
  def playGame(self):
    self.tracker.addLog(LogTypes.GAME_START)
    
    while not self.checkGameEnd(): 
      self.playTurn()

    self.tracker.addLog(LogTypes.GAME_END)
    
  def toDict(self, serializer):
    return {
      "board": serializer(self.board),
      "turnOrder": serializer(self.turnOrder),
      "entityPositions": serializer(self.entityPositions),
      "actionStack": serializer(self.actionStack),
      "turnNumber": serializer(self.turnNumber),
      "roundCount": serializer(self.roundCount),
      "actionsTakenStack": serializer(self.actionsTakenStack),
    }

    
    

  
