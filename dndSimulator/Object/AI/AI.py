import math
from random import random

from dndSimulator.Utils import toDict
from ...Actions import MoveAction


class AI:
  def __init__(self):
    self.reactionGetters = []
    self.actionGetters = []
  
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
  
  def toDict(self, memo, lists):
    return {
      "type": type(self).__name__,
      "reactionGetters": toDict(self.reactionGetters, memo, lists),
      "actionGetters": toDict(self.actionGetters, memo, lists),
    }
  
class RandomMoverAI(AI):
  def getAction(self, game, entity):
    board = game.board
    curSpot = game.getEntityPosition(entity)
    
    moves = []
    
    for neighbor in board.getNeighborsAt(curSpot):
      offSet = curSpot - neighbor
      cost = board.getTileAt(neighbor).getCostFrom(offSet)
      if entity.canPayCost(cost) and game.isActionStackEmpty():
        moves.append(MoveAction(entity, neighbor, curSpot))
    
    if len(moves) == 0:
      return None
    
    return moves[math.floor(random() * len(moves))]