const EntityDisplay = ({entity}) => {
  return (
    <span>
      {
        entity && entity.name
      }
    </span>
  )
}

export default EntityDisplay