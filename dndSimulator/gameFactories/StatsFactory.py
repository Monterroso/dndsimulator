def createStats(speed, backend):
  obj = createRawStats(speed, backend)
  
  return backend.addCompleteObject(obj)

def createRawStats(speed, backend):
  speedIndex = backend.addCompleteObject(speed)
  
  return {"move": speedIndex}