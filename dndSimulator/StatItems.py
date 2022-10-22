from enum import Enum, auto

abilityScores = ["strength", "constitution", "dexterity", "intelligence", "wisdom", "charisma"]

defenses = ["armorClass", "strength", "constitution", "dexterity", "intelligence", "wisdom", "charisma"]

skills = ["initiative"]

class Traits(Enum):
  INCORPOREAL = auto() 