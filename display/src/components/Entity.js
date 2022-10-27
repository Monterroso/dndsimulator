const Entity = ({name, onClick}) => {
  return (
    <span onClick={onClick}>
      {name}
    </span>
  )
}

export default Entity