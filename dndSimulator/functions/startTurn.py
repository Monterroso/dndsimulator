def startTurn(actorIndex, backend):
  #Set the starting actions
  baseStats = backend.getObj(["baseStats"], actorIndex)
  
  backend.setObj(["availableActions"], baseStats, actorIndex)
  
  #Set change block
  backend.endChangeBlock()
  
  