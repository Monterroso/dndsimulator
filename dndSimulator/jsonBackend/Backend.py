class Index:
  def __init__(self, index):
    self.index = index
  
  def __repr__(self) -> str:
    return f"{self.index},,"
  
  def __hash__(self) -> int:
    return self.index
  
  def __eq__(self, __value: object) -> bool:
    return type(__value) == Index and self.index == __value.index
  
  def toJSON(self):
    return self.index
  
#removeObject: workingIndex, trueIndex, object
#addObject: workingIndex
#updateObject: workingIndex, prevIndex, object
#changeParam: workingIndex, paramKey, oldValue, newValue
#addParam: workingIndex, paramKey
#removeParam: workingIndex, paramKey, previousValue
    
class Backend:
  def __init__(self, changes=None, lookupReverse=None, objects=None):
    #List of changes
    self.changes = []
    
    if changes == None:
      self.changes.append([])
    else:
      for changeBlock in changes:
        self.changes.append([])
        for change in changeBlock:
          self.changes[-1].append(self.convertChange(change, Index, self.fixObject))
    
    #Object with working index as key, and true index as value
    self.lookup = {} 
    
    if lookupReverse != None:
      for index, value in enumerate(lookupReverse):
        self.lookup[Index(index)] = Index(value)
    
    
    #List with true index slot with working index
    self.lookupReverse = [] 
    
    if lookupReverse != None:
      for index in lookupReverse:
        self.lookupReverse.append(Index(index))
        
    #List of objects in their true index
    self.objects = [] 
    
    if objects != None:
      for obj in objects:
        self.objects.append({})
        for key, value in obj.items():
          self.objects[-1][Index(key)] = Index(value)
          
    #To hold incompleted objects that should not be indexable until completed
    self.uncompleted = set()
  
  def isPrimitive(self, obj):
    return type(obj) == bool or type(obj) == int or type(obj) == float or type(obj) == str or type(obj) == type(None)
  
  def isObj(self, obj):
    #Check if is a dictionary
    if type(obj) != dict:
      return False
    
    return self.objectIndexChecker(obj)

  def isTup(self, obj):
    #Check if tuple
    if type(obj) != tuple:
      return False
    
    #Ensure all elements are proper indexes
    return self.arrayIndexChecker(obj)
  
  def isValidObj(self, obj):
    return self.isPrimitive(obj) or self.isObj(obj) or self.isTup(obj)
  
  def isValidIndex(self, val):
    """Returns true if the value is a valid Index, value otherwise

    Args:
        val (any): Value to check if Index

    Returns:
        bool: Whether the input val is an Index
    """
    
    if type(val) != Index:
      return False
    
    return val in self.lookup
  
  def arrayIndexChecker(self, arr):
    for val in arr:
      if not self.isValidIndex(val):
        return False

    return True
  
  def objectIndexChecker(self, obj):
    for key, value in obj.items():
      if not self.isValidIndex(key) or not self.isValidIndex(value):
        return False
    
    return True
  
  def getWorkingIndexFromChain(self, chain, startingIndex):
    workingIndex = startingIndex
    
    for key in chain:
      chainIndex = self.addCompleteObject(key) if not self.isValidIndex(key) else key
      workingIndex = self.getFromWorkingIndex(workingIndex)[chainIndex]
      
    return workingIndex
  
  def getIndex(self, chain, startingIndex=Index(0)):
    if not self.isValidIndex(startingIndex):
      raise TypeError(f"The value must not be an index, not a {type(startingIndex)}")
      
    return self.getWorkingIndexFromChain(chain, startingIndex)
  
  def getObj(self, chain, startingIndex=Index(0)):
    workingIndex = self.getIndex(chain, startingIndex)
    
    obj = self.getFromWorkingIndex(workingIndex)
    
    if self.isPrimitive(obj):
      return obj
    
    if type(obj) == tuple:
      return (*obj,)

    return {**obj}
  
  def setIndex(self, chain, setIndex, startingIndex=Index(0)):

    # if not self.arrayIndexChecker(chain):
    #   raise TypeError(f"An element in the array provided is not an index, the types given are {[type(el) for el in chain]}")
    if not self.isValidIndex(startingIndex):
      raise TypeError(f"The value must not be an index, not a {type(startingIndex)}")
    if not self.isValidIndex(setIndex):
      raise TypeError(f"The value must not be an index, not a {type(setIndex)}")
    
    parentIndex = self.getWorkingIndexFromChain(chain[:-1], startingIndex)
    nextIndex = self.addCompleteObject(chain[-1])
    
    if nextIndex not in self.getFromWorkingIndex(parentIndex):
      self.getFromWorkingIndex(parentIndex)[nextIndex] = setIndex
      self.addChange(("addParam", nextIndex, nextIndex, setIndex))
    else:
      prevIndex = self.getFromWorkingIndex(parentIndex)[nextIndex]
      self.getFromWorkingIndex(parentIndex)[nextIndex] = setIndex
      self.addChange(("changeParam", parentIndex, nextIndex, prevIndex, setIndex))
  
  def setObj(self, chain, obj, startingIndex=Index(0)):    
    setIndex = self.addCompleteObject(obj)
    
    return self.setIndex(chain, setIndex, startingIndex)
  
  def removeObjectIndex(self, chain, startingIndex=Index(0)):
    
    # if not self.arrayIndexChecker(chain):
    #   raise TypeError(f"An element in the array provided is not an index, the types given are {[type(el) for el in chain]}")
    if not self.isValidIndex(startingIndex):
      raise TypeError(f"The value must not be an index, not a {type(startingIndex)}")
    
    workingIndex = self.getWorkingIndexFromChain(chain[:-1], startingIndex)
      
    nextIndex = self.addCompleteObject(chain[-1])
    nextIndexValue = self.getFromWorkingIndex(workingIndex)[nextIndex]
    
    del self.getFromWorkingIndex(workingIndex)[nextIndex]
    self.addChange(("removeParam", workingIndex, nextIndex, nextIndexValue))
  
  def getWorkingIndexFromObj(self, obj):
    """Given an object, gets the index within the backend, or -1 if not present

    Args:
        obj (any): object to be compared within backend, check if present

    Raises:
        Exception: If an object given is not of the appropriate type

    Returns:
        Index: Index of object, or -1 if not found
    """
    
    newObj = self.translateObject(obj)
    
    if not self.isValidObj(newObj):
      raise Exception("Object to set is not of the appropriate type")
    
    for trueIndex, testObj in enumerate(self.objects):
      workingIndex = self.lookupReverse[trueIndex]
      
      if type(testObj) == type(newObj):
        if self.isObj(testObj):
          if len(newObj.keys()) == len(testObj.keys()) and workingIndex not in self.uncompleted:
            isCandidate = True
            for key, value in newObj.items():
              if key not in testObj or testObj[key] != value:
                isCandidate = False
                break
            
            if isCandidate:
              return workingIndex
        elif self.isTup(testObj):
          if len(newObj) == len(testObj):
            isCandidate = True
            for i, _ in enumerate(newObj):
              if newObj[i] != testObj[i]:
                isCandidate = False
                break
                
            if isCandidate:
              return workingIndex
        else:
          if newObj == testObj:
            return workingIndex
        
    return -1
  
  def addChange(self, change):
    self.changes[-1].append(change)
  
  def getNextWorkingIndex(self):
    workingIndex = 0
    while Index(workingIndex) in self.lookup:
      workingIndex += 1
      
    return Index(workingIndex)
  
  
  def getFromWorkingIndex(self, workingIndex):
    """Gets the true stored object at given working index

    Args:
        workingIndex (Index): working index to be used to get

    Returns:
        object: returns the actual object if object or tuple
    """
    
    if not self.isValidIndex(workingIndex):
      raise TypeError(f"The value must not be an index, not a {type(workingIndex)}")
    
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
    
    
    if self.isTup(obj):
      return [*obj,]
    
    if self.isPrimitive(obj):
      return []
    
    return [val for val in obj.values()] + [key for key in obj.keys()]
      
  def getObjectsReferenced(self, workingIndex=Index(0)):
    """Generates a set of all workingIndexes that can be accessed from zero index, gets all descendents, and itself

    Args:
        workingIndex (int, optional): index to start recursive searching. Defaults to 0.
        alreadySearched (set, optional): set used to determine which objects have been reached. Defaults to None.

    Returns:
        set: set containing all objects referencable from workingIndex
    """
    
    if not self.isValidIndex(workingIndex):
      raise TypeError(f"The value must not be an index, not a {type(workingIndex)}")
    
    alreadySearched = set()
    
    childIndexes = [workingIndex]
    
    while len(childIndexes) != 0:
      childIndex = childIndexes.pop()
      
      if childIndex not in alreadySearched:
        alreadySearched.add(childIndex)
        childIndexes += self.getChildIndexes(childIndex)
        
    return alreadySearched
        
  def removeUnusedObjects(self):
    """Removes all objects that cannot be accessed from the root
    """
    
    #Gets all the items that are accessible
    accessableItems = self.getObjectsReferenced()
    
    lookups = [key for key in self.lookup.keys()]
    
    for workingIndex in lookups:
      trueIndex = self.lookup[workingIndex]
      #check if reference count is 0
      if workingIndex not in accessableItems:
        
        #Adds the object info for undo, the working and true index, and the object itself shall be stored
        self.addChange(("removeObject", workingIndex, trueIndex, self.getObj([], workingIndex)))
        
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
      
  #Adds generated object, cannot be used for self references, used to check if already in object
  def addCompleteObject(self, obj):
    """Creates new index if not found, or existing if found. Use in all cases if adding without self reference

    Args:
        obj (Any): Object to be added, creates a copy to be used

    Returns:
        Index: working index of added object
    """
    
    newObj = self.translateObject(obj)
    
    if not self.isValidObj(newObj):
      raise TypeError(f"Object to add is not a proper object {newObj}")
    
    #Gets the Index of the object
    workingIndex = self.getWorkingIndexFromObj(newObj)
    
    #If already added, return working Index
    if workingIndex != -1:
      return workingIndex
    
    if self.isTup(newObj):
      newObj = (*newObj,)
    
    if self.isObj(newObj):
      newObj = {**newObj,}
    
    
    #Now we get the reference index, which is the lowest number available
    workingIndex = self.getNextWorkingIndex()
    
    #Sets working index to pair to true index
    self.lookup[workingIndex] = len(self.objects)
    
    #Adds object to lists
    self.objects.append(newObj)
      
    #Set the lookupReverse to be the working index
    self.lookupReverse.append(workingIndex)
    
    #Handle undo
    self.addChange(("addObject", workingIndex, self.getObj([], workingIndex)))
    
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

    for key, value in self.translateObject(params).items():
      self.getFromWorkingIndex(workingIndex)[key] = value
      
    #Sets index to no long be a wip, and thus indexable
    self.uncompleted.remove(workingIndex)
      
    #handle undo
    self.addChange(("updateObject", workingIndex, prev, self.getObj([], workingIndex)))
    
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
    
  def serializeObject(self, obj):
    if type(obj) == dict:
      return {key.toJSON(): val.toJSON() for key, val in obj.items()}
    
    if type(obj) == list:
      return (val.toJSON for val in obj)
    
    if type(obj) == Index:
      a = 1

    return obj
  
  def fixObject(self, obj):
    if type(obj) == dict:
      return {Index(key): Index(val) for key, val in obj.items()}
    
    if type(obj) == list:
      return (Index(val) for val in obj)
    
    if type(obj) == Index:
      a = 1
    
    return obj
  
  def translateObject(self, obj):
    if type(obj) == dict:
      newObj = {}
      
      for key, value in obj.items():
        newKey = key
        newValue = value
        
        if not self.isValidIndex(key):
          newKey = self.addCompleteObject(key)
        if not self.isValidIndex(value):
          newValue = self.addCompleteObject(value)
          
        newObj[newKey] = newValue
          
      return newObj
    
    if type(obj) == list or type(obj) == tuple:
      newObj = []
      
      for value in obj:
        if not self.isValidIndex(value):
          newObj.append(self.addCompleteObject(value))
        else:
          newObj.append(value)
          
      return tuple(newObj)
    
    return obj
       
  def convertChange(self, changeData, IndexClass, fixObjFunction):
    
    op, workingIndex = changeData[:2]
    
    newData = [op, IndexClass(workingIndex)]
    
    if op == "removeObject":
      trueIndex, obj = changeData[2:]
      
      newData.append(trueIndex)
      newData.append(fixObjFunction(obj))
    elif op == "updateObject":
      prevObj, obj = changeData[2:]
      
      newData.append(fixObjFunction(prevObj))
      newData.append(fixObjFunction(obj))
    elif op == "changeParam":
      paramKey, oldValue, newValue = changeData[2:]
      
      newData.append(IndexClass(paramKey))
      newData.append(IndexClass(oldValue))
      newData.append(IndexClass(newValue)) 
    elif op == "addParam":
      paramKey = changeData[2]
      
      newData.append(IndexClass(paramKey))
    elif op == "removeParam":
      paramKey, prevValue = changeData[2:]
      
      newData.append(IndexClass(paramKey))
      newData.append(IndexClass(prevValue))
      
    return tuple(newData)
    
  def writeObject(self, index=Index(0), completedSet=None):
    if type(index) != Index:
      index = Index(index)
      
    if completedSet == None:
      completedSet = {}
      
    if index in completedSet:
      return completedSet[index]
    
    trueIndex = self.lookup[index]
    
    if self.isPrimitive(self.objects[trueIndex]):
      return self.objects[trueIndex]
    
    if self.isTup(self.objects[trueIndex]):
      completedSet[index] = []
      
      for i in self.objects[trueIndex]:
        completedSet[index].append(self.writeObject(i, completedSet))  
    else:
      completedSet[index] = {}
      
      for key, value in self.objects[trueIndex].items():
        completedSet[index][key] = self.writeObject(value, completedSet)
      
    return completedSet[index]
  
  def indexFixer(index):
    if type(index) == Index:
      return index.toJSON()
    
    return index
  
  def serialize(self):
    retObj = {
      "changes": [],
      "lookupReverse": [],
      "objects": [],
    }
    
    for changeBlock in self.changes:
      retObj["changes"].append([])
      for change in changeBlock:
        retObj["changes"][-1].append(self.convertChange(change, lambda x: x.toJSON(), self.serializeObject))
        
    for index in self.lookupReverse:    
      retObj["lookupReverse"].append(index.toJSON())
      
    for obj in self.objects:
      retObj["objects"].append(self.serializeObject(obj))
      
    return retObj