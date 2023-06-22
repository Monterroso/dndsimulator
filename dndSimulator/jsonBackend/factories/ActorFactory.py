def createActor(id, baseStats, ai, backend):
  idIndex = backend.addCompleteObject(id)
  baseStatsIndex = backend.addCompleteObject(baseStats)
  availableActionsIndex = backend.addCompleteObject({})
  aiIndex = backend.addCompleteObject(ai)
  actionIndex = backend.addCompleteObject(None)
  isTurnIndex = backend.addCompleteObject(False)
  
  return backend.addCompleteObject({
    "id": idIndex,
    "baseStats": baseStatsIndex,
    "availableActions": baseStatsIndex,
    "ai": aiIndex,
    "action": actionIndex,
    "isTurn": isTurnIndex,
  })