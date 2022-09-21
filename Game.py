class Game:
  def __init__(self, board):
    self.board = board
      
  def getSpotsValids(self, pos):
    valids = []
    for newx in range(pos.x - 1, pos.y + 2):
      for newy in range(pos.y - 1, pos.y + 2):
        if (newx, newy) not in self.board:
          valids.append([1, (newx, newy)])
          
    return valids
  
