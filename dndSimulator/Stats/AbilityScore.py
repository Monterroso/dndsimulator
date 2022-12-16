from enum import Enum, auto

class AbilityScores(Enum):
  Strength = auto()
  Constitution = auto()
  Dexterity = auto()
  Intelligence = auto()
  Wisdom = auto()
  Charisma = auto()

def getDefaultAbilityScores(default=10):
  return { abilityScore: default for abilityScore in AbilityScores } 