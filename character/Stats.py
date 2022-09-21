from Conditions import SURPRISED

class Stats:
  def __init__(self, abilityScores=None, savingThrows=None, skills=None, reactions=1, actions=1, bonusActions=1, moves=6):
    self.abilityScores = [10 for _ in range(6)] if abilityScores == None else abilityScores
    self.savingThrows = {} if savingThrows == None else savingThrows
    self.skills = {} if skills == None else skills
    self.reactions = reactions
    self.actions = actions
    self.bonusActions = bonusActions
    self.moves = moves
    
  def getConditions(self, gameOjbect):
    return gameOjbect.getConditions()
  
  def getTurnStartActions(self, gameOjbect):
    if SURPRISED in gameOjbect.getConditions():
      return {}
    
    return {
      "reactions": self.reactions,
      "actions": self.actions,
      "bonusActions": self.bonusActions,
      "moves": self.moves
    }
  
  