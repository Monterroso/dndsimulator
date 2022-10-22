from dndSimulator.Utils import toDict
from .Actions import Action, EndTurnAction


class Entity:
  def __init__(self, name, conditions, stats, ai, team):
    self.name = name
    self.ai = ai
    self.currentStats = stats.getBase()
    self.stats = stats
    self.conditions = [stats.filterConditions(conditions)]
    self.availableActions = stats.getTurnStartActions(self)
    self.team = team

  def __repr__(self):
    return self.name
  
  def getTeam(self):
    return self.team

  def getInitiative(self):
    return self.stats.initiative()
  
  def getModifiedStats(self):
    return 
  
  def getStat(self, stat):
    return self.stats.getStat(stat)

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
  
  def attemptDeny(self, denier, action, game):
    return self.stats.attemptDeny(self, denier, action, game)
  
  def attemptPrevent(self, denier, action, game):
    return self.stats.attemptPrevent(self, denier, action, game)
  
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
    
  def toDict(self, memo, lists):
    return {
      "type": type(self).__name__,
      "name": toDict(self.name, memo, lists),
      "ai": toDict(self.ai, memo, lists),
      "stats": toDict(self.stats, memo, lists),
      "conditions": toDict(self.conditions, memo, lists),
      "availableActions": toDict(self.availableActions, memo, lists)
    }