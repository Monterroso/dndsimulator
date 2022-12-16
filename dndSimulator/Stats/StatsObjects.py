from .Stats import Stats
from dndSimulator.Cost import Cost
from .Traits import Traits

actions = Cost()
actions.addCost(6.5, Cost.Features.BASE, Cost.Categories.MOVE)

moveStats = Stats(actions=actions)

ghostMoveStats = Stats(actions=actions, traits=[Traits.INCORPOREAL])