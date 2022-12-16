from .AI import AI
from dndSimulator.ActionGetter import moveAround, denyEnemyMove


moveAIObject = AI()
moveAIObject.addActionGetter(1, moveAround)
moveAIObject.addReactionGetter(1, denyEnemyMove)