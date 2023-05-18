def createBoard(dims, backend):
  dimsIndex = backend.addCompleteObject(dims)
  
  return backend.addCompleteObject({"dims": dimsIndex})