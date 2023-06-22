from . import ActorFactory, BoardFactory, StatsFactory, TupleFactory

def createGame(actors, stats, board, backend):
  gameIndex = backend.createEmpty()
  
  statsDict = {}
  for statsData in stats:
    speed = statsData["move"]
    name = statsData["name"]
    statsDict[name] = StatsFactory.createStatsObject(speed, backend)
  
  actorsList = []
  for actor in actors:
    id = actor["name"]
    baseStats = statsDict[actor["baseStats"]]
    ai = actor["ai"]
    actorsList.append(ActorFactory.createActor(id, baseStats, ai, backend))
    
  actorListIndex = backend.addCompleteObject(tuple(actorsList))
  
  actorPosObj = {}
  for actorIndex in actorsList:
    actorPosObj[actorIndex] = backend.addCompleteObject(TupleFactory.createTuple((0,0,), backend))
    
  actorPosObjIndex = backend.addCompleteObject(actorPosObj)
  
    
  boardIndex = BoardFactory.createBoard(board["dims"], backend)
  
  params = {
    "actors": actorListIndex,
    "currentTurn": backend.addCompleteObject(0),
    "board": boardIndex,
    "actorPos": actorPosObjIndex,
    "actionStack": backend.addCompleteObject(tuple())
  }
  
  backend.completeEmpty(gameIndex, params)
  
  return gameIndex