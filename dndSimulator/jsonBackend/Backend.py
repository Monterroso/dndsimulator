#To create a new item, reserve the index first. Then you build all the components needed, then any additional data
#Two objects, indexes, and non indexes

#First element in objects is constant, cannot be added nor removed, is the initial state.

#Have primitives, list is a primitive with special properties, the list is a list of indexes, object is a list of object

example2 = {
  "changeIndex": 1,
  
  "changes": [
    [["add", ]], [], []
  ],
  
  # If you want the reverse, the right numbers will be sequential, so can make an array, or an object
  "lookup": {
    0: 0,
    1: 1,
    5: 2,
    4: 3,
    3: 4,
  },
  
  "lookupReverse": [0, 1, 5, 4, 3],
  
  #Not necessary to be stored, can be generated from the start, based upon initial state
  "references": {
    1: 1,
    3: 2,
    5: 1,
    4: 1
  },
  
  "objects": [
    {
      "type": "Game",
      "param1": 1,
      "param2": 5,
      "param3": 4,
      "param4": 3
    },
    {
      "type": "A",
      "param9": 3
    },
    {
      "type": "B",
    },
    {
      "type": "C",
    },
    {
      "type": "D",
    }
  ],
  
}


class Backend:
  def __init__(self):
    self.changeIndex = 1
    self.changes = [[]]
    self.lookup = {}
    self.lookupReverse = []
    self.objects = []
    
    self.primitives = ["number", "string", "null", "list"]
    
  def isPrimitive(self, key):
    return key in self.primitives()
  
  def getFromWorkingIndex(self, workingIndex):
    trueIndex = self.lookup[workingIndex]
    
    return self.objects[trueIndex]
    
  def getChildIndexes(self, workingIndex):
    """Returns a list of indexes that are used within the workingIndex object

    Args:
        workingIndex (int): workingIndex of the object we wish to get the children of

    Returns:
        list: list of workingIndexs that are used in this object
    """

    #check if primitive
    obj = self.getFromWorkingIndex(workingIndex)
    
    if self.isPrimitive(obj._type):
      #primitives will have a value parameter
      
      #if a list, we return the list of values held in value
      if obj._type == "list":
        return [val for val in obj.value]
      
      #primitives otherwise have no children indexes
      return []
      
      
    res = []
    #otherwise it's an object
    for key, value in workingIndex.items():
      #ignore the type parameter
      if key != "_type":
        res.append(value)
        
    return res
      
  def getObjectsReferenced(self, workingIndex=0, alreadySearched=None):
    """Generates a set of all workingIndexes that can be accessed from zero index

    Args:
        workingIndex (int, optional): index to start recursive searching. Defaults to 0.
        alreadySearched (set, optional): set used to determine which objects have been reached. Defaults to None.

    Returns:
        set: set containing all objects referencable from workingIndex
    """
    if alreadySearched == None:
      alreadySearched = set()

    alreadySearched.add(workingIndex)
    
    childIndexes = self.getChildIndexes(workingIndex)
    
    for childIndex in childIndexes:
      if childIndex not in alreadySearched:
        self.getObjectsReferenced(childIndex, alreadySearched)
        
    return alreadySearched
        
  
  ###DEPRECIATED  
  def setObjectForRemoval(self, workingIndex):
    """Sets objects for removal by decrementing the reference count of children recursively. \
      Once completed, objects with no references can be removed  

    Args:
        workingIndex (int): workingIndex of object we are setting to remove
    """
    
    removed = set(workingIndex)
    
    childIndexes = self.getChildIndexes(workingIndex)
    
    for childIndex in childIndexes:
      #Decrement the counter for the index
      self.references[childIndex] -= 1
      
      #If counter is 0, then that means that it also needs to be removed
      if self.references[childIndex] == 0:
        self.setObjectForRemoval(childIndex)
        
    
        
  def removeObjects(self):
    """Removes all objects that cannot be accessed from the root
    """
    accessableItems = self.getObjectsReferenced()
    
    for workingIndex, trueIndex in self.lookup.items():
      #check if reference count is 0
      if workingIndex not in accessableItems:
        
        #Adjusts the true index
        indexesNeedingShift = self.lookupReverse[trueIndex + 1:]
        for needsShift in indexesNeedingShift:
          self.lookup[needsShift] -= 1
        
        #Removes from the trueIndex to workingIndex and the objects list
        self.lookupReverse = self.lookupReverse[:trueIndex] + self.lookupReverse[trueIndex + 1:]
        self.objects = self.objects[:trueIndex] + self.objects[trueIndex + 1:]
      
  def endChangeBlock(self):
    """Called when a block is finished executing, cleans up and goes forward
    """
    
    self.removeObjects()
      
    #Make new block to being changed
    self.changes.append([])
    self.changeIndex += 1
    
    
  def addObject(self, type):
    #Now we get the reference index, which is the lowest number available
    workingIndex = 0
    while workingIndex in self.lookup:
      workingIndex += 1
    
    #Adds empty object of type to objects
    self.objects[workingIndex] = {"_type": type}
      
    #Sets working index to pair to true index
    self.lookup[workingIndex] = len(self.objects)
      
    #Set the lookupReverse to be the working index
    self.lookupReverse.append(workingIndex)
    
    return workingIndex
  
  def workingIndexFromObject(self, object):
    """Gets the working index of the object, adds to backend if current does not exist

    Args:
        object (any): item we wish to see if is within our objects list

    Returns:
        int: workingIndex of object
    """
    
    #Check if object is a primitive, and then generate primitive in object format
    return -1
    
  def addToObject(self, workingIndex, params):
    for paramKey, paramValue in params:
      self.objects[workingIndex][paramKey] = self.workingIndexFromObject(paramValue)
    
    
#So, what's the process of creating something in this system? What do we have to do?

backend = Backend()

objectA = {"_type": "A", "paramA": "A"}
objectB = {"_type": "B", "paramB": "B"}
objectAB = {"_type": "AB", "paramA": "A", "paramB": "B"}
object1 = {"_type": 1, "param1": 1}
objectAB1All = {"_type": "AB1", "paramA": objectA, "paramB": objectB, "param1": object1}
objectAB1All["paramSelf"] = objectAB1All

#So, we just want to construct the root
#Then we generate

#So lets say objects have param, with params, they have a type, and they have 

backend.addObject("AB1")

#Create board, will have params
#So first get the placeholder

#Then creates objects based upon the placeholder

#Creates all of the inner objects, with this object as a param

class Creator:
  def __init__(self, type, backend, creator):
    self.backend = backend
    self.type = type
    self.creator = creator
    
  def __call__(self *args, **kwargs):
    
    


def rectangleHolderCreator(backend, rect1params, rect2params, rect3params):
  holder  = backend.addObject()