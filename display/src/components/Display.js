import { useState, useEffect } from "react"
import createGeneralObjectCreator from "../constructors/generalObjectCreator"
import ActionDisplay from "./ActionDisplay"
import BoardDisplay from "./BoardDisplay"
import EntityDisplay from "./EntityDisplay"
import "./Display.css"

const Display = () => {
  const [gameIndex, setGameIndex] = useState(0)
  const [max, setMax] = useState(0)
  const [entityDisplay, setEntityDisplay] = useState()
  const [actionClicked, setActionClicked] = useState()

  const [gameData, setGameData] = useState()

  // Set max
  useEffect(() => {
    fetch("data/text.json")
    .then( response => response.json())
    .then( data => {
      setMax(data.length)
    })
  }, [])

  useEffect(() => {
    fetch("data/text.json")
    .then( response => response.json())
    .then( data => {
      const creator = createGeneralObjectCreator()
      creator.setIndexes(data[gameIndex])
      setGameData(creator.create(0))
    })
  }, [gameIndex])


  if (gameData != null) {
    const actions = gameData.actionsTakenStack

    // Dimenions of the board
    let x = 0
    let y = 0

    // Calculates dimensions of the board
    gameData.board.tiles.forEach(([pos, tile]) => {
      x = Math.max(pos.x)
      y = Math.max(pos.y)
    })

    x += 1
    y += 1

    // Serialized position to entity 
    const posEntity = {}
    gameData.entityPositions.map(([entity, pos]) => {
      pos = `${pos.y} ${pos.x}`
      if (posEntity[pos] == null) {
        posEntity[pos] = []
      }
      posEntity[pos].push(entity)
    })

    return (
      <div>
        <div className="main-display">
          <ActionDisplay actions={actions} clickNum={actionClicked} setClicked={setActionClicked}/>
          <BoardDisplay dims={[x, y]} entityPosObject={posEntity} setEntityDisplay={setEntityDisplay}/>
          <EntityDisplay entity={entityDisplay}/>
        </div>
        <div onClick={() => setGameIndex(value => Math.max(0,value - 1))}>Back</div>
        <div onClick={() => setGameIndex(value => Math.min(max - 1,value + 1))}>Forward</div>
      </div>
    )
  }
  return <div></div>
}

export default Display