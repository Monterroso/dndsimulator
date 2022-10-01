class Logger:
    def __init__(self):
        self.logs = []

    def addLog(self, type, data=None):
        self.logs.append({
            "type": type,
            "data": data
        })

    def printLog(self, filter):
        for log in self.logs:
            if log["type"] in filter:
                print(log["type"])
                if log["data"] != None:
                    print(log["data"])