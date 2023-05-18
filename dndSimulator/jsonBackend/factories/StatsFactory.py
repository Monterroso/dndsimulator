def createStats(speed, backend):
  obj = createStatsObject(speed, backend)
  
  return backend.addCompleteObject(obj)

def createStatsObject(speed, backend):
  speedIndex = backend.addCompleteObject(speed)
  
  return {"move": speedIndex}