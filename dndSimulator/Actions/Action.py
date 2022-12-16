from dndSimulator.Cost import Cost
from dndSimulator.LogTypes import LogTypes

#Base for all actions
class Action:
  """Base Action to be used by all other actions
  """
  def __init__(self, origin=None, parent=None, child=None):
    self.origin = origin
    self.parent = parent
    self.child = child
    self.deniedBy = []
    self.denied = False
    self.preventedBy = []
    self.prevented = False
    
    
  def __eq__(self, other):
    return type(other) == type(self) and self.origin == other.origin \
      and self.parent == other.parent and self.child == other.child \
      and self.deniedBy == other.deniedBy and self.denied == other.denied \
      and self.preventedBy == other.preventedBy and self.prevented == other.prevented
    
  def __repr__(self):
    return "{0}".format(self.__class__.__name__)

  def getCost(self, game):
    """Gets the cost of the action given the game

    Args:
        game (Game): game to get cost from

    Returns:
        Cost: Cost of this action
    """
    return Cost()
  
  def onAdd(self, game, tracker):
    cost = self.getCost(self, game)
    self.origin.payCost(cost)
    tracker.addAction(LogTypes.ACTION_ADDED, {"Action": self, "Cost": cost})
    
  def undoOnAdd(self, tracker):
    actionType, objectInfo, actionInfo = tracker.getRecentAction()
    cost = objectInfo["Cost"]
    self.origin.payCost(-cost)
    tracker.undo()

  def resolveAction(self, game, tracker):
    if self.isDenied():
      self.onDeny(game, tracker)
    elif self.isPrevented():
      self.onPrevent(game, tracker)
    else:
      self.perform(game, tracker)
  
  def perform(self, game, tracker):
    pass
  
  def undoPerform(self, game, tracker):
    pass

  def isValid(self, game):
    return False
  
  def attemptDeny(self, denier, game):
    self.deniedBy.append(denier)
    if self.denyLogic(denier, game):
      self.denied = True
      return True
    return False
  
  def denyLogic(self, denier, game):
    return True
    
  def attemptPrevent(self, preventer, game):
    self.preventedBy.append(preventer)
    self.prevented = True
    return True

  def onPrevent(self, game, tracker):
    if self.origin is not None:
      self.origin.payCost(-self.getCost(game))
      
  def undoOnPrevent(self, game, tracker)
      
  def onDeny(self, game):
    pass
  
  def isPreventer(self, entity):
    if entity in self.preventedBy:
      return True
    return False
    
  def isDenier(self, entity):
    if entity in self.deniedBy:
      return True
    return False
  
  def isPrevented(self):
    return self.prevented
  
  def isDenied(self):
    return self.denied
      
  def setOrigin(self, origin):
    self.origin = origin
    
  def getOrigin(self):
    return self.origin

  def isEntityAction(self):
    return self.origin == None
  
  def toDict(self, serializer):
    return {
      "origin": serializer(self.origin),
      "parent": serializer(self.parent),
      "child": serializer(self.child),
      "deniedBy": serializer(self.deniedBy),
      "denied": serializer(self.denied),
      "preventedBy": serializer(self.preventedBy),
      "prevented": serializer(self.prevented),
    }
  
  @classmethod
  def isAction(cls, action):
    return issubclass(type(action), cls)