from dndSimulator.Cost import Cost
import uuid

#Base for all actions
class Action:
  def __init__(self, origin=None, parent=None, child=None):
    self.origin = origin
    self.parent = parent
    self.child = child
    self.deniedBy = []
    self.denied = False
    self.preventedBy = []
    self.prevented = False
    self.id = uuid.uuid1()
    
  def getId(self):
    return self.id
    
  def __eq__(self, other):
    return type(other) == type(self) and self.getId() == other.getId()
    
  def __repr__(self):
    return "{0}".format(self.__class__.__name__)

  def getCost(self, game):
    return Cost()

  def resolveAction(self, game):
    if self.isDenied():
      self.onDeny(game)
    if self.isPrevented():
      self.onPrevent(game)
    else:
      self.perform(game)
  
  def perform(self, game):
    pass
  
  def getNextAction(self, game):
    return None

  def isValid(self, game):
    return False
  
  def attemptDeny(self, denier, game):
    self.deniedBy.append(denier)
    self.denied = True
    return True
    
  def attemptPrevent(self, preventer, game):
    self.preventedBy.append(preventer)
    self.prevented = True
    return True

  def onPrevent(self, game):
    if self.origin is not None:
      self.origin.payCost(-self.getCost(game))
      
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
      "id": serializer(self.id),
      "deniedBy": serializer(self.deniedBy),
      "denied": serializer(self.denied),
      "preventedBy": serializer(self.preventedBy),
      "prevented": serializer(self.prevented),
    }
  
  @classmethod
  def isAction(cls, action):
    return issubclass(type(action), cls)

  @classmethod
  def isValidAction(cls, action, game):
    return  cls.isAction(action) and action.isValid(game)