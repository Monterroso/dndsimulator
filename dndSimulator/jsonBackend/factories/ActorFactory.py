def createActor(id, baseStats, ai, backend):
  idIndex = backend.addCompleteObject(id)
  baseStatsIndex = backend.addCompleteObject(baseStats)
  availableActionsIndex = backend.addCompleteObject({})
  aiIndex = backend.addCompleteObject(ai)
  
  return backend.addCompleteObject({"id": idIndex, "baseStats": baseStatsIndex, "availableActions": availableActionsIndex, "ai": aiIndex})