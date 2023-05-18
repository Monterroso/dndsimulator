class Backend:
  def __init__(self):
    self.changes = [[]]
    #Object with working index as key, and true index as value
    self.lookup = {}
    #List with true index slot with working index
    self.lookupReverse = []
    #List of objects in their true index
    self.objects = []
    
    self.uncompleted = set()
  
  def isPrimitive(self, obj):
    return "value" in obj and len(obj) == 1
  
  def isList(self, obj):
    return self.isPrimitive(obj) and type(obj["value"]) == tuple
  
  def getIndex(self, chain, startingIndex=0):
    workingIndex = startingIndex
    
    for key in chain:
      workingIndex = self.getFromWorkingIndex(workingIndex)[key]
      
    return workingIndex
  
  def getObj(self, chain, startingIndex=0):
    workingIndex = self.getIndex(chain, startingIndex)
    
    obj = self.getFromWorkingIndex(workingIndex)
    
    if self.isPrimitive(obj):
      return obj["value"]
    
    return obj
  
  def setIndex(self, chain, setIndex, startingIndex=0):
    workingIndex = startingIndex
    
    for key in chain[:-1]:
      workingIndex = self.getFromWorkingIndex(workingIndex)[key]
    
    if chain[-1] not in self.getFromWorkingIndex(workingIndex):
      self.getFromWorkingIndex(workingIndex)[chain[-1]] = setIndex
      self.addChange(("addParam", workingIndex, chain[-1], setIndex))
    else:
      prevIndex = self.getFromWorkingIndex(workingIndex)[chain[-1]]
      self.getFromWorkingIndex(workingIndex)[chain[-1]] = setIndex
      self.addChange(("changeParam", workingIndex, chain[-1], prevIndex, setIndex))
  
  def setObj(self, chain, obj, startingIndex=0):
    setIndex = self.addCompleteObject(obj)
    
    return self.setIndex(chain, setIndex, startingIndex)
  
  def remove(self, chain, startingIndex=0):
    workingIndex = startingIndex
    
    for key in chain[:-1]:
      workingIndex = self.getFromWorkingIndex(workingIndex)[key]
      
    prevIndex = self.getFromWorkingIndex(workingIndex)[chain[-1]]
    
    del self.getFromWorkingIndex(workingIndex)[chain[-1]]
    self.addChange(("removeParam", workingIndex, chain[-1], prevIndex))
  
  def getWorkingIndexFromObj(self, obj):
    for trueIndex, testObj in enumerate(self.objects):
      workingIndex = self.lookupReverse[trueIndex]
      if len(obj.keys()) == len(testObj.keys()) and workingIndex not in self.uncompleted:
        isCandidate = True
        for key, value in obj.items():
          if key not in testObj or testObj[key] != value:
            isCandidate = False
            break
        
        if isCandidate:
          return workingIndex
        
    return -1
  
  def addChange(self, change):
    self.changes[-1].append(change)
  
  def getNextWorkingIndex(self):
    workingIndex = 0
    while workingIndex in self.lookup:
      workingIndex += 1
      
    return workingIndex
  
  
  def getFromWorkingIndex(self, workingIndex):
    trueIndex = self.lookup[workingIndex]
    
    return self.objects[trueIndex]
    
  def getChildIndexes(self, workingIndex):
    """Returns a list of indexes that are used within the workingIndex object, gets immediate children only

    Args:
        workingIndex (int): workingIndex of the object we wish to get the children of

    Returns:
        list: list of workingIndexs that are used in this object
    """

    #check if primitive
    obj = self.getFromWorkingIndex(workingIndex)
    
    
    if self.isList(obj):
      return [val for val in obj["value"]]
    
    if self.isPrimitive(obj):
      return []
      
    res = []
    #otherwise it's an object
    for _, value in obj.items():
      res.append(value)
        
    return res
      
  def getObjectsReferenced(self, workingIndex=0, alreadySearched=None):
    """Generates a set of all workingIndexes that can be accessed from zero index, gets all descendents, and itself

    Args:
        workingIndex (int, optional): index to start recursive searching. Defaults to 0.
        alreadySearched (set, optional): set used to determine which objects have been reached. Defaults to None.

    Returns:
        set: set containing all objects referencable from workingIndex
    """
    if alreadySearched == None:
      alreadySearched = set()

    alreadySearched.add(workingIndex)
    
    childIndexes = self.getChildIndexes(workingIndex)
    
    for childIndex in childIndexes:
      if childIndex not in alreadySearched:
        self.getObjectsReferenced(childIndex, alreadySearched)
        
    return alreadySearched
        
  def removeUnusedObjects(self):
    """Removes all objects that cannot be accessed from the root
    """
    
    #Gets all the items that are accessible
    accessableItems = self.getObjectsReferenced()
    
    lookups = [*self.lookup.keys()]
    
    for workingIndex in lookups:
      trueIndex = self.lookup[workingIndex]
      #check if reference count is 0
      if workingIndex not in accessableItems:
        
        #Adds the object info for undo, the working and true index, and the object itself shall be stored
        self.addChange(("removeObject", workingIndex, trueIndex, {**self.objects[trueIndex]}))
        
        #Adjusts the true index
        indexesNeedingShift = self.lookupReverse[trueIndex + 1:]
        
        for needsShift in indexesNeedingShift:
          self.lookup[needsShift] -= 1
        
        #Remove from lookup
        del self.lookup[workingIndex]
        
        #Removes from the trueIndex to workingIndex and the objects list
        self.lookupReverse.pop(trueIndex)
        self.objects.pop(trueIndex)
      
  def endChangeBlock(self):
    """Called when a block is finished executing, cleans up and goes forward
    """
    
    self.removeUnusedObjects()
      
    #Make new block to being changed
    self.changes.append([])
    
  def makePrimitive(self, value):
    return {"value": value}
      
  #Adds generated object, cannot be used for self references, used to check if already in object
  def addCompleteObject(self, obj):
    """Creates new index if not found, or existing if found. Use in all cases if adding without self reference

    Args:
        obj (dict): Either created object with keys, or object to be converted to a primitive

    Returns:
        int: working index of added object
    """
    
    #Check if obj is not a dict, and handle
    if type(obj) != dict:
      obj = self.makePrimitive(obj)
    
    if not self.isPrimitive(obj):
      for _, value in obj.items():
        if type(value) != int:
          raise Exception("An improper object attempting to be added")
    
    newObj = {**obj}
    
    for key, value in newObj.items():
      if type(value) == list:
        newObj[key] = tuple(value)
    
    #Gets the hash of the object
    workingIndex = self.getWorkingIndexFromObj(newObj)
    
    if workingIndex != -1:
      return workingIndex
    
    
    #Now we get the reference index, which is the lowest number available
    workingIndex = self.getNextWorkingIndex()
    
    #Sets working index to pair to true index
    self.lookup[workingIndex] = len(self.objects)
    
    #Adds object to lists
    self.objects.append(newObj)
      
    #Set the lookupReverse to be the working index
    self.lookupReverse.append(workingIndex)
    
    #Handle undo
    self.addChange(("addObject", workingIndex, {**self.getFromWorkingIndex(workingIndex)}))
    
    return workingIndex
    
  
  def createEmpty(self):
    """Creates an empty space for an object to be added. Used for self referential and base object. \
      Don't use this if former not the case

    Returns:
        int: workingIndex of empty object
    """
    
    workingIndex = self.getNextWorkingIndex()
    
    obj = {}
    
    #Sets working index to pair to true index
    self.lookup[workingIndex] = len(self.objects)
    
    #Adds object to lists
    self.objects.append(obj)
    
    #Ensure the backend knows this index is a wip, and not indexable
    self.uncompleted.add(workingIndex)
      
    #Set the lookupReverse to be the working index
    self.lookupReverse.append(workingIndex)

    #Handle Undo
    self.addChange(("addObject", workingIndex, {}))
    
    return workingIndex
  
  def completeEmpty(self, workingIndex, params):
    """Adds parameters to an empty object, and ensures can be looked up via hash

    Args:
        workingIndex (int): workingIndex of the empty object
        params (dict): object to be used as the parameters of the object at workingIndex
    """
    
    if self.getWorkingIndexFromObj(params) != -1:
      raise Exception("Item added but same was added causing a duplication")
    
    prev = {**self.getFromWorkingIndex(workingIndex)}

    for key, value in params.items():
      self.getFromWorkingIndex(workingIndex)[key] = value
      
    #Sets index to no long be a wip, and thus indexable
    self.uncompleted.remove(workingIndex)
      
    #handle undo
    self.addChange(("updateObject", workingIndex, prev, {**self.getFromWorkingIndex(workingIndex)}))
    
  def undo(self):
    def removeObj(workingIndex):
      del self.lookup[workingIndex]
      
      self.objects.pop()
      self.lookupReverse.pop()
      
    for change in self.changes[-1][::-1]:
      if change[0] == "removeObject":
        workingIndex, trueIndex, obj = change[1:]
        
        for needsShift in self.lookupReverse[trueIndex:]:
          self.lookup[needsShift] += 1
        
        self.lookup[workingIndex] = trueIndex
        
        self.lookupReverse.insert(trueIndex, workingIndex)
        self.objects.insert(trueIndex, obj)
      elif change[0] == "addObject":  
        workingIndex = change[1]
        
        removeObj(workingIndex)
      elif change[0] == "updateObject":
        workingIndex, prev = change[1:3]
        
        trueIndex = self.lookup[workingIndex]
        self.objects[trueIndex] = prev
      elif change[0] == "changeParam":
        workingIndex, nextName, prev = change[1:]
        
        self.getFromWorkingIndex(workingIndex)[nextName] = prev
      elif change[0] == "addParam":
        workingIndex, nextName = change[1:]
        
        del self.getFromWorkingIndex(workingIndex)[nextName]
      elif change[0] == "removeParam":
        workingIndex, nextName, prev = change[1:]
        
        self.getFromWorkingIndex(workingIndex)[nextName] = prev
          
      
    self.changes.pop()
    
def createPrimitive(val):
  if type(val) == list:
    return {"value": tuple(val)}
  
  return {"value": val}   

class Index:
  def __init__(self, index):
    self.index = index

if __name__ == "__main__":

  backend = Backend()

  first = backend.createEmpty()

  #Got the index of the first, now create the others
  a = backend.addCompleteObject({"value": 1})
  b = backend.addCompleteObject({"value": 2})
  backend.addCompleteObject({"a": a, "b": b})
  ab = backend.addCompleteObject({"a": a, "b": b})

  backend.completeEmpty(first, {"a": a, "b": b, "ab": ab, "H": first})

  backend.setObj(["H"], {"value": 2})

  backend.endChangeBlock()

  d = backend.addCompleteObject({"value": 4})
  c = backend.addCompleteObject({"value": 3})

  backend.setObj(["ab", "a"], {"value": 3})
  
  backend.endChangeBlock()

  e = backend.addCompleteObject({"value": 5})
  f = backend.addCompleteObject({"value": 6})
  
  backend.endChangeBlock()