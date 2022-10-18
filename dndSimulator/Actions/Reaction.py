from .Action import Action
from .PostAction import PostAction


class Reaction(Action):
  def getNextAction(self, game):
    return PostAction(self)