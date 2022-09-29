from Actions import Action, EndTurnAction


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

    if Action.isValid(reaction, game, self):
      return reaction
  
  def getAction(self, game):
    #Called when they take their turn, should return some sort of action, returning none ends the turn
    action = self.ai.getAction(game, self)

    if Action.isValid(action, game, self):
      return action