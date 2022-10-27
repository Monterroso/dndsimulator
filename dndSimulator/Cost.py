from enum import Enum, auto
import copy

class Cost:
  class Categories(Enum):
    STANDARD = auto()
    MOVE = auto()
    BONUS = auto()
    REACTION = auto()

  class Features(Enum):
    BASE = auto()

  def __init__(self, isInfinite=False):
    self.costs = {}

    self.isInfinite = isInfinite

  def __add__(self, other):
    if self.isInfinite or other.isInfinite:
      return Cost(isInfinite=True)

    costObject = copy.deepcopy(self)
    
    for category, featureCost in other.costs.items():
      for feature, cost in featureCost.items():
        costObject.addCost(cost, feature, category)
    
    return costObject

  def __sub__(self, other):
    if self.isInfinite or other.isInfinite:
      return Cost(isInfinite=True)

    costObject = copy.deepcopy(self)
    
    for category, featureCost in other.costs.items():
      for feature, cost in featureCost.items():
        costObject.subCost(cost, feature, category)
    
    return costObject

  def setInfinite(self):
    self.isInfinite = True

  def isValid(self):
    if self.isInfinite:
      return False

    for _, featureCost in self.costs.items():
      for _, cost in featureCost.items():
        if cost < 0:
          return False

    return True
      
  def addCost(self, cost, feature, category):
    if category not in self.costs:
      self.costs[category] = {}

    if feature not in self.costs[category]:
      self.costs[category][feature] = 0
        
    self.costs[category][feature] += cost

  def subCost(self, cost, feature, category):
    self.addCost(-cost, feature, category)
      
  def toDict(self, serializer):
    return {
      "costs": serializer(self.costs)
    }