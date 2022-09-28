class Logger:
    def __init__(self):
        self.logs = []

    def addLog(self, type, data=None):
        self.logs.append({
            "type": type,
            "data": data
        })

    def printLog(self):
        for log in self.logs:
            print(log["type"])
            print(log["data"])