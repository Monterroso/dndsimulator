import "./EntityDisplay.css"

const EntityDisplay = ({entity}) => {
  return (
    <span className="entity-display">
      {
        entity && entity.name
      }
    </span>
  )
}

export default EntityDisplay