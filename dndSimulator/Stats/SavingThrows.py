from enum import Enum, auto
from .AbilityScore import AbilityScores

class SavingThrows(Enum):
  StrengthSave = auto()
  ConstitutionSave = auto()
  DexteritySave = auto()
  IntelligenceSave = auto()
  WisdomSave = auto()
  CharismaSave = auto()

allSavingThrowsWithStat = {
  SavingThrows.StrengthSave: AbilityScores.Strength,
  SavingThrows.ConstitutionSave: AbilityScores.Constitution,
  SavingThrows.DexteritySave: AbilityScores.Dexterity,
  SavingThrows.IntelligenceSave: AbilityScores.Intelligence,
  SavingThrows.WisdomSave: AbilityScores.Wisdom,
  SavingThrows.CharismaSave: AbilityScores.Charisma,
}

def getDefaultSavingThrowBonus(default=0):
  return {save: default for save in allSavingThrowsWithStat}