def getCurrentTurnId(backend):
  turn = backend.backend.getObj(["currentTurn"])
  actors = backend.backend.getObj(["actors"])
  actorIndex = actors[turn]
  actorId = backend.backend.getObj(["id"], actorIndex)
  return actorId