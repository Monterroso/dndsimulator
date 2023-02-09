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
    self.deniedBy = set()
    self.deniedByFailed = set()
    self.preventedBy = set()
    self.preventedByFailed = set()
    
  def __eq__(self, other):
    return type(other) == type(self) and self.origin == other.origin \
      and self.parent == other.parent and self.child == other.child \
      and self.deniedBy == other.deniedBy and self.deniedByFailed == other.deniedByFailed \
      and self.preventedBy == other.preventedBy and self.preventedByFailed == other.preventedByFailed
    
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
    cost = self.getCost(game)
    oldActions = self.origin.payCost(cost)
    tracker.addAction(LogTypes.ACTION_ADDED, {"Action": self, "NewCost": cost, "OldActions": oldActions})
    
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
      
  def undoResolveAction(self, game, tracker):
    if self.isDenied():
      self.undoOnDeny(game, tracker)
    elif self.isPrevented():
      self.undoOnPrevent(game, tracker)
    else:
      self.undoPerform(game, tracker)
  
  def perform(self, game, tracker):
    tracker.addAction(LogTypes.ACTION_PERFORMED, {"Action": self})
  
  def undoPerform(self, game, tracker):
    tracker.undo()

  def isValid(self, game):
    return False
  
  def attemptDeny(self, denier, game):
    
    if self.denyLogic(denier, game):
      self.deniedBy.add(denier)
      return True
    
    self.deniedByFailed.add(denier)
    return False
  
  def undoAttemptDeny(self, denier, game):
    if denier in self.deniedBy:
      self.deniedBy.remove(denier)
      
    if denier in self.deniedByFailed:
      self.deniedByFailed.remove(denier)
  
  def denyLogic(self, denier, game):
    return True
  
  def preventLogic(self, preventer, game):
    return True
    
  def attemptPrevent(self, preventer, game):
    if self.preventLogic(preventer, game):
      self.preventedBy.add(preventer)
      return True
    
    self.preventedByFailed.add(preventer)
    return False
  
  def undoAttemptPrevent(self, preventer, game):
    if preventer in self.preventedBy:
      self.preventedBy.remove(preventer)
      
    if preventer in self.preventedByFailed:
      self.preventedByFailed.remove(preventer)

  def onPrevent(self, game, tracker):
    if self.origin is not None:
      cost = -self.getCost(game)
      self.origin.payCost(cost)
      tracker.addAction(LogTypes.ACTION_PREVENTED, {"Action": self, "Cost": cost})
      
  def undoOnPrevent(self, game, tracker):
    if self.origin is not None:
      self.origin.payCost(self.getCost(game))
      tracker.undo()
      
  def onDeny(self, game, tracker):
    tracker.addAction(LogTypes.ACTION_DENIED, {"Action": self})
  
  def undoOnDeny(self, game, tracker):
    tracker.undo()
  
  def isPreventer(self, entity):
    if entity in self.preventedBy:
      return True
    return False
  
  def hasAttemptedPrevent(self, entity):
    return entity in self.preventedBy or entity in self.preventedByFailed
    
  def isDenier(self, entity):
    if entity in self.deniedBy:
      return True
    return False
  
  def hasAttemptedDeny(self, entity):
    return entity in self.deniedBy or entity in self.deniedByFailed
  
  def isPrevented(self):
    return len(self.preventedBy) > 0
  
  def isDenied(self):
    return len(self.deniedBy) > 0
      
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
      "deniedByFailed": serializer(self.deniedByFailed),
      "preventedBy": serializer(self.preventedBy),
      "preventedByFailed": serializer(self.preventedByFailed),
    }
  
  @classmethod
  def isAction(cls, action):
    return issubclass(type(action), cls)