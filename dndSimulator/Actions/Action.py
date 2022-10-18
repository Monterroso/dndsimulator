from dndSimulator.Cost import Cost
from dndSimulator.Results import Result

#Base for all actions
class Action:
  def __init__(self):
    self.origin = None
    
  def __eq__(self, other):
    if type(self) != type(other):
      return False
    
    for property, value in vars(self).iteritems():
      if getattr(other, property) != value:
        return False
      
    return True
    
  def __repr__(self):
    return "{0}".format(self.__class__.__name__)

  def getCost(self, game):
    return Cost()

  def resolveAction(self, game):
    return Result(self, {})
  
  def getNextAction(self, game):
    return None

  def isValid(self, game):
    return False

  def onPrevent(self, game):
    if self.origin is not None:
      self.origin.payCost(-self.getCost(game))
      
  def setOrigin(self, origin):
    self.origin = origin

  def isEntityAction(self):
    return self.origin == None
  
  def serialize(self, serializer):
    serializer.startObject(None, repr(self))
    serializer.addProperty("origin", self.origin)
  
  @classmethod
  def isAction(cls, action):
    return issubclass(type(action), cls)

  @classmethod
  def isValidAction(cls, action, game):
    return  cls.isAction(action) and action.isValid(game)