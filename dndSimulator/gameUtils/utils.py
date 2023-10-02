def getDistance(pos1, pos2):
  if len(pos1) != len(pos2):
    raise Exception("Cant get distance of positions of different dimensions ${pos1} and ${pos2}")
  
  diff = []
  for index in range(len(pos1)):
    diff.append(abs(pos1[index] - pos2[index]))
    
  return (max(diff) / 2) + (sum(diff) / 2)

def decompactTupe(tup, backend):
  newTup = []
  
  for index in tup:
    newTup.append(backend.getObj([], index))
    
  return tuple(newTup)

def getHash(obj):
  result = ""
  if type(obj) == dict:
    keys = obj.keys()
    keys.sort()

    for key in keys:
      result += getHash(obj[key])
  elif type(obj) == tuple or type(obj) == list:
    for val in obj:
      result += getHash(val)
  else:
    result += obj
    
  return result

