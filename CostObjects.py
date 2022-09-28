from Cost import Cost

ZeroCost = Cost()
OneMoveCost = Cost()
OneMoveCost.addCost(1, Cost.Features.BASE, Cost.Categories.MOVE)
OneAndHalfMoveCost = Cost()
OneAndHalfMoveCost.addCost(1.5, Cost.Features.BASE, Cost.Categories.MOVE)