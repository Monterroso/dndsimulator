from .Serialize.Serializer import Serializer

class Tracker:
  def __init__(self):
    self.serializer = Serializer()
    self.actionList = []
    
  def addObject(self, obj):
    self.serializer(obj)

  def addAction(self, actionType, objectInfo=None, actionInfo=None):
    objectInfo = {} if objectInfo == None else objectInfo
    actionInfo = {} if actionInfo == None else actionInfo
    
    self.serializer.startRecord()
    
    curatedObjectInfo = {}
    
    for objName, obj in objectInfo.items():
      self.serializer(obj)
      curatedObjectInfo[objName] = self.getIndex(obj)
      
    self.actionList.append([int(actionType), curatedObjectInfo, actionInfo])
    
  def appendToAction(self, objectInfo=None, actionInfo=None):
    objectInfo = {} if objectInfo == None else objectInfo
    actionInfo = {} if actionInfo == None else actionInfo
    
    for objName, obj in objectInfo.items():
      self.serializer(obj)
      self.actionList[-1][1][objName] = self.getIndex(obj)
      
    for actName, actData in actionInfo.items():
      self.actionList[-1][2][actName] = actData
    
  def getIndex(self, item):
    return self.serializer.getIndex(item)
    
  def getRecentAction(self):
    return self.actionList[-1]
    
  def undo(self):
    self.serializer.removePrevious()
    self.actionList.pop()
    
  def getSerialized(self):
    return {
      **self.serializer.getInfo(),
      "actionList": self.actionList,
    }
    
  def getTurnByTurn(self, turn):
    indexes = None
    
    if turn == 0:
      indexes = self.serializer.getAllDependentIndexes(self.serializer.getFirstIndexes())
    else:
      indexes = self.serializer.getAllDependentIndexes(set(i for i in self.actionList[turn][1].values()))
      
    return {index: self.serializer.getObject(index) for index in indexes}
      
    
    
  
  