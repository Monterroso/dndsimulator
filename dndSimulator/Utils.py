class Serializer:
  def __init__(self):
    self.memo = []
    self.lists = []
    
  def __call__(self, obj):
    if obj not in self.memo:
      item = {
        "type": type(obj).__name__,
      }
      
      self.memo.append(obj)
      self.lists.append(item)
      
      if hasattr(obj, "toDict"):
        for key, value in obj.toDict(self).items():
          item[key] = value
          
      elif isinstance(obj, dict):
        item["pairs"] = []
        for key, value in obj.items():
          item["pairs"].append((self(key), self(value)))
      
      else:
        #Check if iteratable
        try:
          iterator = iter(obj)
          item["items"] = []
          for value in iterator:
            item["items"].append(self(value))
            
        #Otherwise
        except TypeError:
           item["value"] = repr(obj)
    
    return {"index": self.memo.index(obj)}
  
  def getResult(self):
    return self.lists