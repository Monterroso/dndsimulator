from .Actions import Action, EndTurnAction, MoveAction, StartTurnAction
from dndSimulator.Stats import Traits, allSavingThrowsWithStat, allSkillsWithStat

class Entity:
  def __init__(self, name, stats, ai, team):
    self.name = name
    self.ai = ai
    self.stats = stats
    self.availableActions = self.getTurnStartActions()
    self.team = team
    self.equipment = []
    
    self.turnBroken = False

  def __repr__(self):
    return self.name
  
  def getTeam(self):
    return self.team

  def getAbilityScoreModifier(self, abilityScore):
    return self.stats.getAbilityScoreModifier(abilityScore)
  
  def getSavingThrow(self, savingThrow):
    stat = allSavingThrowsWithStat[savingThrow]
    return self.getAbilityScoreModifier(stat) + self.stats.getSavingThrowBonus(savingThrow)
  
  def getSkill(self, skill):
    stat = allSkillsWithStat[skill]
    return self.getAbilityScoreModifier(stat) + self.stats.getSkillBonus(skill)
  
  def getTurnStartActions(self):
    return self.stats.getActions()
  
  def getAvailableActions(self):
    return self.availableActions
  
  def setAvailableActions(self, newAvailableActions):
    oldActions = self.availableActions
    self.availableActions = newAvailableActions
    
    return oldActions

  def startTurn(self):
    return self.setAvailableActions(self.getTurnStartActions())
    
  def undoStartTurn(self, oldActions):
    self.setAvailableActions(oldActions)

  def getModifiedCost(self, cost):
    return cost

  def canPayCost(self, cost):
    newCost = self.getModifiedCost(cost)
    nextCost = self.availableActions - newCost

    return nextCost.isValid()

  def payCost(self, cost):
    oldCost = self.availableActions
    newCost = self.getModifiedCost(cost)
    self.availableActions -= newCost
    
    return oldCost
  
  def attemptDeny(self, denier, action, game):
    if type(action) == MoveAction:
      if Traits.INCORPOREAL in self.stats.traits:
        return False
      return True
    
    return True
  
  def attemptPrevent(self, preventer, action, game):
    return True
  
  def getReaction(self, game):
    reaction = self.ai.getReaction(game, self)

    if Action.isAction(reaction):
      reaction.setOrigin(self)
      
      if reaction.isValid(game):
        return reaction
  
  def getAction(self, game):
    if self.turnBroken == False:
      self.turnBroken = True
      return StartTurnAction(self)
    
    action = self.ai.getAction(game, self)
    
    if Action.isAction(action):
      action.setOrigin(self)
      
      if action.isValid(game):
        return action
      
    self.turnBroken = False
    return EndTurnAction(self)
    
  def toDict(self, serializer):
    return {
      "name": serializer(self.name),
      "ai": serializer(self.ai),
      "stats": serializer(self.stats),
      "availableActions": serializer(self.availableActions),
      "team": serializer(self.team),
      "equipment": serializer(self.equipment),
      "turnBroken": serializer(self.turnBroken)
    }