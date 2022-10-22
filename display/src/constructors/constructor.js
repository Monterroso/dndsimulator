const constructor = (data) => {
  const constList = data.map(obj => {

  })

  data.map((obj, index) => {
    constList[index]
  })
}

class GameObjectCreator {
  constructor() {
    this.registers = {}
  }

  registerCreator(key, creator) {
    this.registers[key] = creator
  }

  create(obj) {
    const creator = this.registers[obj.type]
    
    
  }
}