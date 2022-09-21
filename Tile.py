class Tile:
  def __init__(self, neighbors, height=0, objects=None, partialBlocks=None, mostlyBlocks=None, totalBlocks=None):
    self.height = height
    self.neighbors = neighbors
    self.partialBlocks = [] if partialBlocks == None else partialBlocks
    self.mostlyBlocks = [] if mostlyBlocks == None else mostlyBlocks
    self.totalBlocks = [] if totalBlocks == None else totalBlocks
    self.objects = [] if objects == None else objects
    
  def getHeight(self):
    return self.height
  
  def getPartialBlocks(self):
    return self.partialBlocks
  
  def getMostlyBlocks(self):
    return self.mostlyBlocks
  
  def getTotalBlocks(self):
    return self.totalBlocks
  
  def getObjects(self):
    return self.objects
  
  def getCostDirectionTo(self, tileOrientation):
    return MoveObject()
  