from Conditions import SURPRISED
from Cost import Cost

class Stats:
  def __init__(self, abilityScores=None, savingThrows=None, skills=None, actions=None):
    self.abilityScores = [10 for _ in range(6)] if abilityScores == None else abilityScores
    self.savingThrows = {} if savingThrows == None else savingThrows
    self.skills = {} if skills == None else skills
    self.actions = actions if actions is not None else {}
    

  def initiative(self):
    return self.abilityScores[2]
    
  def getConditions(self, entity):
    return self.filterConditions(entity.getConditions())

  def filterConditions(self, conditions):
    return conditions

  def getModifiedCost(self, cost):
    return cost

  def getTurnStartActions(self, entity):
    if SURPRISED in self.getConditions(entity):
      return Cost()
    
    return self.actions
  
  