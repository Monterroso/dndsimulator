

import math
from random import random
from Actions import MoveAction


class AI:
  def __init__(self):
    pass
  
  def getReaction(self, game, entity):
    pass
    
  def getAction(self, game, entity):
    #If the execute stack is empty, means it is your turn to act, otherwise you have to react to something else
    pass
  
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