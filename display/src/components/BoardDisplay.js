import TileDisplay from "./TileDisplay"
import "./BoardDisplay.css"


const BoardDisplay = ({dims, entityPosObject, setEntityDisplay}) => {
  const [x, y] = dims
  const tileArray = new Array(y).fill(new Array(x).fill(0))

  return (
    <div className="board">
      {
        tileArray.map((row, rowIndex) => (
          <div className="tile-row"> 
            {
              row.map((_, colIndex) => {
                const entities = entityPosObject[`${rowIndex} ${colIndex}`] || []
                return <TileDisplay key={rowIndex + " " + colIndex} entities={entities} setEntityDisplay={setEntityDisplay}/>
              })
            }
          </div>
          
        ))
      }
    </div>
  )
}

export default BoardDisplay