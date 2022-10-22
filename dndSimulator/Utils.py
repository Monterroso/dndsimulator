def toDict(toConvert, memo, lists):
  if toConvert in memo:
    return {"index": memo.index(toConvert)}
    
  item = {
    "type": type(toConvert).__name__,
  }
  
  curIndex = len(memo)
  
  memo.append(toConvert)
  lists.append(item)
  
  
  if hasattr(toConvert, "toDict"):
    for key, value in toConvert.toDict(memo, lists).items():
      item[key] = value
  elif isinstance(toConvert, dict):
    item["pairs"] = []
    
    for key, value in toConvert.items():
      item["pairs"].append((toDict(key, memo, lists), toDict(value, memo, lists)))
  elif isinstance(toConvert, list):
    item["items"] = []
    
    for value in toConvert:
      item["items"].append(toDict(value, memo, lists))
  else:
    item["value"] = repr(toConvert)
  
  return {"index": curIndex}
    