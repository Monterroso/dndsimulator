import Entity from "./Entity"
import "./TileDisplay.css"

const Tile = ({entities, setEntityDisplay}) => {
  return (
    /* <span style={{width: "200px", height: "200px", backgroundColor: "red", display: "inline-block"}}> */
    <span className="tile">
      {entities.map((entity, index) => {
        return <Entity key={index} name={entity.name} onClick={() => setEntityDisplay(entity)}/>
      })}
    </span>
  )
}

export default Tile