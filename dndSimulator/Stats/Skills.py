from enum import Enum, auto
from .AbilityScore import AbilityScores

class Skills(Enum):
  Initiative = auto()

allSkillsWithStat = {
  Skills.Initiative: AbilityScores.Dexterity
}
  
def getDefaultSkillBonus(default=0):
  return {skill: default for skill in allSkillsWithStat}