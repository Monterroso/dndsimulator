from .Action import Action

class PostAction(Action):
  def __init__(self, action):
    self.action = action
    
    super().__init__()
  
  def isValid(self, game):
    return False
  
  def toDict(self, serializer):
    return {
      **super().toDict(serializer),
      "action": serializer(self.action),
    }