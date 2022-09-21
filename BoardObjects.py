class BoardObject:
  def __init__(self, conditions, stats, ai, position):
    self.ai = ai
    self.stats = stats
    self.conditions = [stats.getConditions(conditions)]
    self.availableActions = [stats.getStartActions(self.conditions)]
    self.position = position
  
  def takeAction(self, game):
    #Called when they take their turn, should return some sort of action, returning none ends the turn
    action = self.ai.getAction()
    
    