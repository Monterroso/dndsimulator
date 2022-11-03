import classNames from "classnames"
import "./ActionDisplay.css"

const getBaseActionAttributes = (action) => {
  const attrs = []

  attrs.push([`Origin: ${action.origin.name != null ? action.origin.name : action.origin.type}`])
  
  if (action.parent != null) {
    attrs.push([`Parent: ${action.parent.id}`])
  }

  if (action.child != null) {
    attrs.push([`Child: ${action.child.id}`])
  }

  if (action.denied !== 0) {
    attrs.push(["Denied: True"])
  }
  
  if (action.deniedBy != null) {
    attrs.push(["Denied By:"])
    action.deniedBy.map(({name}) => attrs[attrs.length - 1].push(name))
  }

  if (action.prevented !== 0) {
    attrs.push(["Prevented: True"])
  }

  if (action.preventedBy != null) {
    action.preventedBy.map(({name}) => attrs[attrs.length - 1].push(name))
  }

  return attrs
}

const ActionDisplay = ({actions, clickNum, setClicked}) => {
  return (
    <div className="action-display">
      {actions.map((action, index) => {
        return (
          <div className={classNames("action", {highlighted: clickNum === index})} onClick={() => setClicked(index)}>
            {action.type}
            {
              clickNum === index && (
                getBaseActionAttributes(action).map((block) => {
                  return (
                    <div>
                      {
                        block
                      }
                    </div>
                  )
                })
              )
            }
          </div>
        )
      })}
    </div>
  )
}

export default ActionDisplay