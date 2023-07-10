def startTurn(actorIndex, backend):
  #Set the starting actions
  baseStats = backend.getObj(["baseStats"], actorIndex)
  
  backend.setObj(["availableActions"], baseStats, actorIndex)
  
  backend.setObj(["turnStarted"], True)