class ActionHandler:
  def __init__(self, data=None):
    self.actionDict = {**data[0]} if data != None else {}
    self.hasHit = set(data[1]) if data != None else set()
    
  def popAction(self, actorId):

    self.hasHit.add(actorId)

    if actorId not in self.actionDict:
      return ["none", []]

    retAction = self.actionDict[actorId]

    del self.actionDict[actorId]

    return retAction
  
  def setAction(self, actorId, actionData):
    self.actionDict[actorId] = actionData
    if actorId in self.hasHit:
      self.hasHit.remove(actorId)

  def canSkip(self, actorId):
    """Called if we can pause execution 

    Can be called once and return true, all other calls will be false

    An action can be delayed once, but if ran again and no action set, we assume no action taken

    Args:
        actorId (any): identifier used for an actor pair combo

    Returns:
        boolean: whether we want to skip to get an action, or use the current action (or no action)
    """

    canSkip = actorId in self.hasHit

    if actorId in self.hasHit:
      self.hasHit.remove(actorId)

    return canSkip

  def serialize(self):
    return [{**self.actionDict}, list(self.hasHit)]
