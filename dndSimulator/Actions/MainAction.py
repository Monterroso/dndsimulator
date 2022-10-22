from .Action import Action

#Base action types
class MainAction(Action):
  def isValid(self, game):
    if game.isActionStackEmpty():
      return True
    return False