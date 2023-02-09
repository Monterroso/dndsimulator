class Serializer:
  def __init__(self, objectList=None):
    self.objectList = [] if objectList == None else objectList
    self.memo = []
    self.addedObjects = [0]
    
  def __call__(self, obj):
    if obj not in self.memo:
      item = {
        "type": type(obj).__name__,
      }
      
      self.memo.append(obj)
      self.objectList.append(item)
      self.addedObjects[-1] += 1
      
      if hasattr(obj, "toDict"):
        for key, value in obj.toDict(self).items():
          item[key] = value
          
      elif isinstance(obj, dict):
        item["pairs"] = []
        for key, value in obj.items():
          item["pairs"].append((self(key), self(value)))
      
      elif isinstance(obj, list) or isinstance(obj, tuple):
        item["items"] = []
        for value in obj:
          item["items"].append(self(value))
          
      else:
        item["value"] = repr(obj)
    
    return {"index": self.memo.index(obj)}
  
  def getResult(self):
    return self.objectList
  
  def getIndex(self, item):
    return self.memo.index(item)
  
  def getObject(self, index):
    return self.objectList[index]
  
  def getFirstIndexes(self):
    return {i for i in range(self.addedObjects[0])}
  
  def getAllDependentTurn(self, indexes):
    searchIndexes = set(*indexes)
    searchedSet = set()
    
    while len(searchIndexes) != 0:
      index = searchIndexes.pop()
      searchedSet.add(index)
      
      for _, value in self.objectList[index].items():
        if isinstance(value, dict):
          for keyName, indexValue in value.items():
            if keyName == "index" and indexValue not in searchedSet:
              searchIndexes.add(indexValue)

    return searchedSet
  
  def removePrevious(self):
    """Removes the elements of the last record session
    """
    self.memo = self.memo[:len(self.memo) - self.addedObjects[-1]]
    self.objectList = self.objectList[:len(self.objectList) - self.addedObjects[-1]]
    self.addedObjects.pop()
      
  
  def startRecord(self):
    """Starts a session of recording new added objects. Calling this function when a new action is performed, before objects from action are added
    """
    self.addedObjects.append(0)
    
  def getInfo(self):
    return {
      "addedObjects": self.addedObjects,
      "objectList": self.objectList
    }
    