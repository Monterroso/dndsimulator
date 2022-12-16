from queue import PriorityQueue

def sumCosts(positions, game, entity):
  """A simple metric which sums all of the costs associated along the path, if an enemy is in the way counts as blocked

  Args:
      positions (List<Position>): List of Positions representing the path to evaluate
      game (Entity): Game in question
      entity (Entity): Entity to be traveling

  Returns:
      Float: Result of the sum of all the costs traversing the path
  """
  
  curCost = 0
  
  for i in range(len(positions) - 1):
    cost = game.getCostFrom(positions[i], positions[i + 1], entity)
    
    # Checks if part of the path cannot be physically reached
    if cost.isInfinite():
      return float("inf")
    
    # Checks if an enemy is in the way
    obEntities = game.getEntitiesAt(positions[i + 1])
    for obEntity in obEntities:
      if obEntity.team != entity.team:
        return float("inf")
      
      
    curCost += cost.sumUp()
    
  return curCost

def djkistras(origin, destination, game, entity, metric=sumCosts):
  """Performs djikstras on the board from origin to destination, with a specific metric

  Args:
      origin (Position): Position to start off for the djikstras
      destination (Position): Position serving as destination for the djikstras
      game (Game): Game in question
      entity (Entity): Entity to be moved
      metric (lambda, optional): Function taking a path and returning a distance value. Defaults to sumCosts.

  Returns:
      List<Position>: List of Positions as the shortest path given the metric, empty if no path was found
  """
  
  priorQueue = PriorityQueue()
  visited = set()
  
  priorQueue.put((metric([origin], game, entity), [origin]))
  
  while not priorQueue.empty():
    nodeList = priorQueue.get()
    lastNode = nodeList[-1]
    
    if lastNode == destination:
      return nodeList
    
    visited.add(lastNode)
    neighbors = game.board.getNeighborsAt(lastNode)
    
    for neighbor in neighbors:
      if neighbor not in visited:
        priorQueue.put((metric([*nodeList, neighbor], game, entity), [*nodeList, neighbor]))
        
  return []
    