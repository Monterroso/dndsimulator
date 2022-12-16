class Serializer:
  def __init__(self, objectList=None):
    self.objectList = [] if objectList == None else objectList
    self.memo = {}
    self.addedObjects = []
    
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
    
    return {"index": self.objectList.index(obj)}
  
  def getResult(self):
    return self.objectList
  
  def getIndex(self, item):
    return self.memo.index(item)
  
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