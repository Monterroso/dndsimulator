from .Stats import Stats
from .Cost import Cost

actions = Cost()
actions.addCost(6.5, Cost.Features.BASE, Cost.Categories.MOVE)

moveStats = Stats(actions=actions)