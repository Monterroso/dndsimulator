import json

class JSONSerializer:
  def __init__(self):
    self.currentObject = None
    
  def startObject(self, objectName, objectId):
    self.currentObject = {
      "id": objectId
    }
    
  def addProperty(self, name, value):
    self.currentObject[name] = value
    
  def toString(self):
    return json.dumps(self.currentObject)