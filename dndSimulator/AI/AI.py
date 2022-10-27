class AI:
  def __init__(self):
    self.reactionGetters = []
    self.actionGetters = []
    self.data = {}
    
  def getData(self):
    return self.data
  
  def addActionGetter(self, priority, actionGetter):
    self.actionGetters.append((priority, actionGetter))
    self.actionGetters.sort(key=lambda tup: tup[0])
    
  def addReactionGetter(self, priority, actionGetter):
    self.reactionGetters.append((priority, actionGetter))
    self.reactionGetters.sort(key=lambda tup: tup[0])
    
  def getAction(self, game, entity):
    for _, actionGetter in self.actionGetters:
      action = actionGetter(game, entity)
      if action != None:
        return action
  
  def getReaction(self, game, entity):
    for _, actionGetter in self.reactionGetters:
      action = actionGetter(game, entity)
      if action != None:
        return action
  
  def toDict(self, serializer):
    return {
      "reactionGetters": serializer(self.reactionGetters),
      "actionGetters": serializer(self.actionGetters),
    }