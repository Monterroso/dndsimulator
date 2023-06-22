def endTurn(backend):
  turn = backend.getObj(["currentTurn"])
  actors = backend.getObj(["actors"])
  actorIndex = actors[turn]
  
  backend.setObj(["isTurn"], False, actorIndex)
  
  newTurnNumber = (turn + 1) % len(actors)
  backend.setObj(["currentTurn"], newTurnNumber)
  backend.endChangeBlock()