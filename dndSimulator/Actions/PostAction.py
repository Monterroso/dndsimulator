from dndSimulator.Utils import toDict
from .Action import Action


class PostAction(Action):
  def __init__(self, action):
    self.action = action
    
    super().__init__()
  
  def isValid(self, game):
    return False
  
  def toDict(self, memo, lists):
    return {
      **super().toDict(memo, lists),
      "action": toDict(self.action, memo, lists),
    }