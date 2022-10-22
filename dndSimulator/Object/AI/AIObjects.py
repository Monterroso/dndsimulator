from .AI import AI
from .ActionGetter import randomMove, denyEnemyMove


moveAIObject = AI()
moveAIObject.addActionGetter(1, randomMove)
moveAIObject.addReactionGetter(1, denyEnemyMove)