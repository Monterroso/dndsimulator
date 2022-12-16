from .Serialize.Serializer import Serializer

class Tracker:
  def __init__(self):
    self.serializer = Serializer()
    self.actionList = []

  def addAction(self, actionType, objectInfo=None, actionInfo=None):
    objectInfo = {} if objectInfo != None else objectInfo
    actionInfo = {} if actionInfo != None else actionInfo
    
    self.serializer.startRecord()
    
    for objName, obj in objectInfo.items():
      self.serializer(obj)
    
    self.actionList.append([actionType, {objName: self.tracker.getIndex(obj) for objName, obj in objectInfo.items()}, actionInfo])
    
  def getIndex(self, item):
    self.serializer.getIndex(item)
    
  def getRecentAction(self):
    return self.actionList[-1]
    
  def undo(self):
    self.serializer.removePrevious()
    self.actionList.pop()
    
  
  