from .Action import Action
from .PostAction import PostAction

#Base action types
class MainAction(Action):
  def getNextAction(self, game):
    return PostAction(self)
  
  def isValid(self, game):
    if game.isActionStackEmpty():
      return True
    return False