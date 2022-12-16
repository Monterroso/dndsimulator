from enum import Enum, auto
import copy

class Cost:
  """A cost object contains cost information
  
  First layer is the category, then the feature with cost
  
  An infinite cost is always invalid, and infinite cost is always an infinite cost
  """
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
    
  def isInfinite(self):
    return self.isInfinite

  def isValid(self):
    """Determines whether the cost object is valid, if any of the features are negative or is infinite

    Returns:
        Boolean: Whether the cost object is valid
    """
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
    
  def sumUp(self):
    sumVal = 0
    for _, featureCost in self.costs.items():
      for _, cost in featureCost.items():
        sumVal += cost
        
    return sumVal
      
      
  def toDict(self, serializer):
    return {
      "costs": serializer(self.costs)
    }