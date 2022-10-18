import json


class Logger:
    def __init__(self):
        self.logs = []

    def addLog(self, type, data=None):
        self.logs.append({
            "type": type,
            "data": data
        })

    def printLog(self, *, filter=[], dataFilter=[]):
        for log in self.logs:
            if log["type"] in filter and log["type"] not in dataFilter:
                print(log["type"])
                if log["data"] != None:
                    print(log["data"])
                    
    def serialize(self, serializer):
        serializer.startObject(None, repr(self))
        serializer.addProperty("logs", "")#json.dumps(self.logs))