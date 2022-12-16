from dndSimulator.Serialize.Serializer import Serializer


class Logger:
  def __init__(self):
    self.logs = []
    self.serializes = []

  def addLog(self, logType, data=None):
    self.logs.append({
      "logType": logType,
      "data": data
    })

  def getLog(self, *, filter=[], dataFilter=[]):
    logs = []
    for log in self.logs:
      if log["logType"] in filter and type(log["data"]) not in dataFilter:
        logs.append([log["logType"]])
        if log["data"] != None:
          logs[-1].append((log["data"]))
                
    return logs
                  
  def getSerialized(self):
    return self.serializes
      
  def serialize(self, item):
    serializer = Serializer()
    serializer(item)
    
    self.serializes.append(serializer.getResult())