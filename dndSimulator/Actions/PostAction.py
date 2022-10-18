from ..Serializer import objectSerializer
from .Action import Action


class PostAction(Action):
  def __init__(self, action):
    self.action = action
    
    super().__init__()
  
  def isValid(self, game):
    return True
  
  def serialize(self, serializer):
    serializer.startObject(None, repr(self))
    serializer.addProperty("action", objectSerializer.serialize(self.action))