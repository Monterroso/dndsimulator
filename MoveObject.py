class MoveObject:
  def __init__(self, startpos, endpos):
    self.startpos = startpos
    self.endpos = endpos
    self.costs = {}
    
  def __add__(self, other):
    moveObj = None
    if other.startpos == self.endpos:
      moveObj = MoveObject(self.startpos, other.endpos)
      
    if other.endpos == self.startpos:
      moveObj = MoveObject(other.startpos, self.endpos)
      
    if moveObj == None:
       raise Exception('These Move Objects cannot be combined as their start and ends do not overlap')
     
    for feature, cost in self.costs:
      moveObj.addCost(cost, feature)
      
    for feature, cost in other.costs:
      moveObj.addCost(cost, feature)
      
    return moveObj
      
  def addCost(self, cost, feature):
    if feature not in self.costs:
      self.costs[feature] = 0
      
    self.costs[feature] += cost