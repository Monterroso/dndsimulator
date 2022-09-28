from Actions import EndTurnAction


class Entity:
  def __init__(self, conditions, stats, ai, logger):
    self.ai = ai
    self.stats = stats
    self.conditions = [stats.filterConditions(conditions)]
    self.availableActions = stats.getTurnStartActions(self)
    self.logger = logger

  def getInitiative(self):
    return self.stats.initiative()

  def startTurn(self):
    self.availableActions = self.stats.getTurnStartActions(self)

  def getConditions(self):
    return self.conditions

  def canPayCost(self, cost):
    return self.stats.canPayCost(cost)

  def canPayCost(self, cost):
    newCost = self.stats.getModifiedCost(cost)
    nextCost = self.availableActions - newCost

    return nextCost.isValid()

  def payCost(self, cost):
    newCost = self.stats.getModifiedCost(cost)
    self.currentActions = self.availableActions - newCost
  
  def getAction(self, game):
    #Called when they take their turn, should return some sort of action, returning none ends the turn
    action = self.ai.getAction(game, self)


    if action is not None and action.isValid(game, self):
      return action

    if self == game.getCurrentEntityTurn() and game.isActionStackEmpty():
      return EndTurnAction()
    
    