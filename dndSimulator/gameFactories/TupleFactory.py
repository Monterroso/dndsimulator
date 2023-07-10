def createTuple(tup, backend):
  return tuple([backend.addCompleteObject(val) for val in tup])