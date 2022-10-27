class GeneralObjectCreator {
  constructor() {
    this.registers = {}
    this.memo = []
  }

  setIndexes(indexes) {
    this.indexes = indexes
  }

  setDefault(creator) {
    this.default = creator
  }

  registerCreator(key, creator) {
    this.registers[key] = creator
  }

  create(index) {
    const memobj = this.memo[index]
    if (memobj != null) {
      return memobj
    }

    const obj = this.indexes[index]
    const creator = this.registers[obj.type]
    
    if (creator == null) {
      return this.default.create(obj, this)
    }
    return creator.create(obj, this)
  }
}

class ArtificalCreator {
  create(obj, objectCreator) {
    const createdObject = {}
    
    Object.keys(obj).forEach(key => {
      if (key !== "type") {
        createdObject[key] = objectCreator.create(obj[key].index)
      }
      else {
        createdObject[key] = obj[key]
      }
    })
    
    return createdObject
  }
}

class ValueCreator {
  constructor(cast) {
    this.cast = cast
  }
  create(obj, objectCreator) {
    return this.cast(obj.value)
  }
}

class DictCreator {
  create(obj, objectCreator) {
    const retList = []
    obj.pairs.forEach(([key, value]) => {
      retList.push([objectCreator.create(key.index), objectCreator.create(value.index)])
    })
    return retList
  }
}

class ListCreator {
  create(obj, objectCreator) {
    return obj.items.map(item => objectCreator.create(item.index))
  }
}

const ArtificialObjects = ["Game", "Board", "Position", "Tile", "Cost", "Entity", "AI", "Stats", "StartTurnAction", "MoveAction", "EndTurnAction"]

const numCreator = new ValueCreator(val => Number(val))
const strCreator = new ValueCreator(val => String(val))
const nullCreator = new ValueCreator(() => undefined)

const createGeneralObjectCreator = () => {
  const generalObjectCreator = new GeneralObjectCreator()
  ArtificialObjects.forEach(key => generalObjectCreator.registerCreator(key, new ArtificalCreator()))
  generalObjectCreator.registerCreator("Categories", strCreator)
  generalObjectCreator.registerCreator("Features", strCreator)
  generalObjectCreator.registerCreator("str", strCreator)
  generalObjectCreator.registerCreator("int", numCreator)
  generalObjectCreator.registerCreator("float", numCreator)
  generalObjectCreator.registerCreator("NoneType", nullCreator)
  generalObjectCreator.registerCreator("dict", new DictCreator())
  generalObjectCreator.registerCreator("list", new ListCreator())
  generalObjectCreator.registerCreator("tuple", new ListCreator())
  generalObjectCreator.setDefault(strCreator)

  return generalObjectCreator
}

export default createGeneralObjectCreator
