from dndSimulator.Actions.MoveAction import MoveAction
from copy import deepcopy
from dndSimulator.Conditions import SURPRISED
from dndSimulator.Cost import Cost
from .AbilityScore import getDefaultAbilityScores
from .SavingThrows import getDefaultSavingThrowBonus
from .Skills import getDefaultSkillBonus

class Stats:
  def __init__(self, abilityScores=None, savingThrowsBonus=None, skillsBonus=None, actions=None, traits=None):
    self.abilityScores = getDefaultAbilityScores() if abilityScores == None else abilityScores
    self.savingThrowsBonus = getDefaultSkillBonus() if savingThrowsBonus == None else savingThrowsBonus
    self.skillsBonus = getDefaultSkillBonus() if skillsBonus == None else skillsBonus
    self.actions = actions if actions is not None else {}
    self.traits = traits if traits is not None else []

  def getAbilityScoreModifier(self, abilityScore):
    return (self.abilityScores[abilityScore] - 10) // 2
  
  def getSavingThrowBonus(self, savingThrow):
    return self.savingThrowsBonus[savingThrow]
  
  def getSkillBonus(self, skill):
    return self.skillsBonus[skill]
  
  def getTraits(self):
    return self.traits
  
  def getActions(self):
    return deepcopy(self.actions)
  
  def toDict(self, serializer):
    return {
      "abilityScores": serializer(self.abilityScores),
      "savingThrowsBonus": serializer(self.savingThrowsBonus),
      "skillsBonus": serializer(self.skillsBonus),
      "actions": serializer(self.actions),
      "traits": serializer(self.traits)
    }