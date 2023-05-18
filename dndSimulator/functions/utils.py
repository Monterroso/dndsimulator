def getDistance(pos1, pos2):
  total = 0
  for i in range(len(pos1)):
    total += abs(pos1[i] - pos2[i])
    
  return total