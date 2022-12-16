from .Action import Action

#Base action types
class MainAction(Action):
  """Action to be used for main actions on an empty stack, may be removed in future
  """
  def isValid(self, game):
    if game.isActionStackEmpty():
      return True
    return False