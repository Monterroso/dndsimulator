"""Action Getters return an action given a game and an entity, used in composition within AI objects"""
from .RandomMove import getAction as randomMove
from .DenyEnemyMove import denyEnemyMove
from .MoveAround import getAction as moveAround