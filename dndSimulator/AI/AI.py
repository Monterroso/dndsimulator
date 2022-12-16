class AI:
  """Used to generate actions based upon a game state
  """
  def __init__(self):
    self.reactionGetters = []
    self.actionGetters = []
  
  def addActionGetter(self, priority, actionGetter):
    """Adds an action getter to the AI with a given priority (lower values resolved first)

    Args:
        priority (int): priority for which the action getter should be accessed
        actionGetter (ActionGetter): function return an action
    """
    
    self.actionGetters.append((priority, actionGetter))
    self.actionGetters.sort(key=lambda tup: tup[0])
    
  def addReactionGetter(self, priority, actionGetter):
    """Adds an action getter to the AI with a given priority (lower values resolved first)

    Args:
        priority (int): priority for which the action getter should be accessed
        actionGetter (ActionGetter): function return an action
    """
    
    self.reactionGetters.append((priority, actionGetter))
    self.reactionGetters.sort(key=lambda tup: tup[0])
    
  def getAction(self, game, entity):
    """Calls the action getters based upon priority, and returns an action

    Args:
        game (Game): Current game state
        entity (Entity): Entity AI is attached to

    Returns:
        Action: Action to be returned
    """
    
    for _, actionGetter in self.actionGetters:
      action = actionGetter(game, entity)
      return action
  
  def getReaction(self, game, entity):
    """Calls the reaction getters based upon priority, and returns an action

    Args:
        game (Game): Current game state
        entity (Entity): Entity AI is attached to

    Returns:
        Action: Action to be returned
    """
    for _, actionGetter in self.reactionGetters:
      action = actionGetter(game, entity)
      return action
  
  def toDict(self, serializer):
    return {
      "reactionGetters": serializer(self.reactionGetters),
      "actionGetters": serializer(self.actionGetters),
    }