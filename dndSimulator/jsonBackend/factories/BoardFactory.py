from . import TupleFactory

def createBoard(dims, backend):
  dimsIndex = backend.addCompleteObject(TupleFactory.createTuple(dims, backend))
  
  return backend.addCompleteObject({"dims": dimsIndex})