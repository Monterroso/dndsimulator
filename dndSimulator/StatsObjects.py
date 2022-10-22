from .Stats import Stats
from .Cost import Cost
from .StatItems import Traits

actions = Cost()
actions.addCost(6.5, Cost.Features.BASE, Cost.Categories.MOVE)

moveStats = Stats(actions=actions)

ghostMoveStats = Stats(actions=actions, traits=[Traits.INCORPOREAL])