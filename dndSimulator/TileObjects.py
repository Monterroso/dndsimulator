from .Cost import Cost
from .CostObjects import ZeroCost, OneMoveCost, OneAndHalfMoveCost
from .Tile import Tile


from .PositionObjects import TopLeftPosition, TopPosition, TopRightPosition, LeftPosition, OriginPosition, RightPosition, BottomLeftPosition, BottomPosition, BottomRightPosition 


TLP = {TopLeftPosition: OneAndHalfMoveCost}
TP = {TopPosition: OneMoveCost}
TRP = {TopRightPosition: OneAndHalfMoveCost}

LP = {LeftPosition: OneMoveCost}
EP = {OriginPosition: ZeroCost}
RP = {RightPosition: OneMoveCost}

BLP = {BottomLeftPosition: OneAndHalfMoveCost}
BP = {BottomPosition: OneMoveCost}
BRP = {BottomRightPosition: OneAndHalfMoveCost}

def createMoveData(*posCosts):
  posCostObj = {} 
  for posCost in posCosts:
    for pos in posCost:
      posCostObj[pos] = posCost[pos]

  return posCostObj



TopLeftTile = Tile(createMoveData(BP, BRP, RP))
TopTile = Tile(createMoveData(LP, BLP, BP, BRP, RP))
TopRightTile = Tile(createMoveData(LP, BLP, BP))

LeftTile = Tile(createMoveData(TP, TRP, RP, BRP, BP))
InnerTile = Tile(createMoveData(TLP, TP, TRP, RP, BRP, BP, BLP, LP))
RightTile = Tile(createMoveData(BP, BLP, LP, TLP, TP))

BottomLeftTile = Tile(createMoveData(TP, TRP, RP))
BottomTile = Tile(createMoveData(LP, TLP, TP, TRP, RP))
BottomRightTile = Tile(createMoveData(LP, TLP, TP))

SingleRowLeftTile = Tile(createMoveData(RP))
SingleRowInnerTile = Tile(createMoveData(LP, RP))
SingleRowRightTile = Tile(createMoveData(LP))

SingleColumnTopTile = Tile(createMoveData(BP))
SingleColumnInnerTile = Tile(createMoveData(BP, TP))
SingleColumnBotTile = Tile(createMoveData(TP))

SingleTile = Tile(createMoveData())

