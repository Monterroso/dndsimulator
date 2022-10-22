const constructor = (data) => {
  const constList = data.map(obj => {

  })

  data.map((obj, index) => {
    constList[index]
  })
}

class GameObjectCreator {
  constructor(indexes) {
    this.registers = {}
    this.indexes = indexes
  }

  registerCreator(key, creator) {
    this.registers[key] = creator
  }

  create(obj) {
    const creator = this.registers[obj.type]
    
    return creator(obj, this)
  }
}

gameCreator = (obj, objectCreator) => {
  const createdObject = {}
  createdObject["board"] = 
  return {
    "type": type(self).__name__,
    "board": toDict(self.board, memo, lists),
    "turnOrder": toDict(self.turnOrder, memo, lists),
    "entityPositions": toDict(self.entityPositions, memo, lists),
    "actionStack": toDict(self.actionStack, memo, lists),
    "turnNumber": toDict(self.turnNumber, memo, lists),
    "roundCount": toDict(self.roundCount, memo, lists),
    "actionsTakenStack": toDict(self.actionsTakenStack, memo, lists),
  }
}