from dndSimulator.Actions.MoveAction import MoveAction
from dndSimulator.Utils import toDict
from copy import deepcopy
from .Conditions import SURPRISED
from .Cost import Cost
from .StatItems import Traits

class Stats:
  def __init__(self, abilityScores=None, savingThrows=None, skills=None, actions=None, traits=None):
    self.abilityScores = [10 for _ in range(6)] if abilityScores == None else abilityScores
    self.savingThrows = {} if savingThrows == None else savingThrows
    self.skills = {} if skills == None else skills
    self.actions = actions if actions is not None else {}
    self.traits =  traits if traits is not None else []
  
  def getBase(self):
    return {"abilityScores": self.abilityScores,}  
  
  def initiative(self):
    return self.abilityScores[2]
  
  def getStat(self, stat):
    if stat in self.savingThrows:
      return self.savingThrows[stat]
    if stat in self.skills:
      return self.skills[stat]
    
  def getConditions(self, entity):
    return self.filterConditions(entity.getConditions())

  def filterConditions(self, conditions):
    return conditions

  def getModifiedCost(self, cost):
    return cost
  
  def attemptDeny(self, entity, denier, action, game):
    if type(action) == MoveAction:
      if Traits.INCORPOREAL in self.traits:
        return False
      return True
    
    return True
  
  def attemptPrevent(self, entity, denier, action, game):
    return True
      

  def getTurnStartActions(self, entity):
    if SURPRISED in self.getConditions(entity):
      return Cost()
    
    return deepcopy(self.actions)
  
  def toDict(self, memo, lists):
    return {
      "type": type(self).__name__,
      "abilityScores": toDict(self.abilityScores, memo, lists),
      "savingThrows": toDict(self.savingThrows, memo, lists),
      "skills": toDict(self.skills, memo, lists),
      "actions": toDict(self.actions, memo, lists),
    }
    
  
  