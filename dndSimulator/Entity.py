from .Serializer import objectSerializer
from .Actions import Action, EndTurnAction


class Entity:
  def __init__(self, name, conditions, stats, ai, logger):
    self.name = name
    self.ai = ai
    self.stats = stats
    self.conditions = [stats.filterConditions(conditions)]
    self.availableActions = stats.getTurnStartActions(self)
    self.logger = logger

  def __repr__(self):
    return "Entity: {0}".format(self.name)

  def getInitiative(self):
    return self.stats.initiative()

  def startTurn(self):
    self.availableActions = self.stats.getTurnStartActions(self)

  def getConditions(self):
    return self.conditions

  def getModifiedCost(self, cost):
    return self.stats.getModifiedCost(cost)

  def canPayCost(self, cost):
    newCost = self.getModifiedCost(cost)
    nextCost = self.availableActions - newCost

    return nextCost.isValid()

  def payCost(self, cost):
    newCost = self.stats.getModifiedCost(cost)
    self.availableActions -= newCost
  
  def getReaction(self, game):
    reaction = self.ai.getReaction(game, self)
    
    if Action.isAction(reaction):
      reaction.setOrigin(self)

    if Action.isValidAction(reaction, game):
      return reaction
  
  def getAction(self, game):
    #Called when they take their turn, should return some sort of action, returning none ends the turn
    action = self.ai.getAction(game, self)
    
    if Action.isAction(action):
      action.setOrigin(self)

    if Action.isValidAction(action, game):
      return action
    
  def serialize(self, serializer):    
    serializer.startObject(None, repr(self))
    
    serializer.addProperty("name", self.name)
    serializer.addProperty("ai", objectSerializer.serialize(self.ai))
    serializer.addProperty("stats", objectSerializer.serialize(self.stats))
    serializer.addProperty("conditions", self.conditions)
    serializer.addProperty("availableActions", objectSerializer.serialize(self.availableActions))
    serializer.addProperty("logger", objectSerializer.serialize(self.logger))
    