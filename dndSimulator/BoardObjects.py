from .Board import Board
from .Position import Position
from .TileObjects import BottomLeftTile, BottomRightTile, BottomTile, InnerTile, LeftTile, RightTile, SingleColumnBotTile, SingleColumnInnerTile, SingleColumnTopTile, SingleRowInnerTile, SingleRowLeftTile, SingleRowRightTile, SingleTile, TopLeftTile, TopRightTile, TopTile


def createBotRow(width):
  first, *inner, last = [Position(0, 0), *[Position(i, 0) for i in range(1, width - 1)], Position(width - 1, 0)]

  return [(first, BottomLeftTile), *[(ins, BottomTile) for ins in inner], (last, BottomRightTile)]

def createTopRow(width, height):
  first, *inner, last = [Position(0, height - 1), *[Position(i, height - 1) for i in range(1, width - 1)], Position(width - 1, height - 1)]

  return [(first, LeftTile), *[(ins, InnerTile) for ins in inner], (last, RightTile)]

def createInnerRow(width, level):
  first, *inner, last = [Position(0, level), *[Position(i, level) for i in range(1, width - 1)], Position(width - 1, level)]

  return [(first, TopLeftTile), *[(ins, TopTile) for ins in inner], (last, TopRightTile)]

def createSingleRow(width):
  first = Position(0, 0)
  inner = [Position(i, 0) for i in range(1, width - 1)]
  last = Position(width - 1, 0)

  return [(first, SingleRowLeftTile), *[(ins, SingleRowInnerTile) for ins in inner], (last, SingleRowRightTile)]

def createSingleColumn(height):
  first = Position(0, 0)
  inner = [Position(0, i) for i in range(1, height - 1)]
  last = Position(0, height - 1)

  return [(first, SingleColumnBotTile), *[(ins, SingleColumnInnerTile) for ins in inner], (last, SingleColumnTopTile)]

def createSingleBoard():
  single = Position(0,0)

  return [(single, SingleTile)]

def createBoard(width, height):
  if width <= 0 or height <= 0:
    raise TypeError("A board cannot be created with a dimenion less than 1")

  if width == 1 and height == 1:
    return createSingleBoard()

  if width == 1:
    return createSingleColumn(height)

  if height == 1:
    return createSingleRow(width)

  positionTileList = []

  for posTile in createBotRow(width):
    positionTileList.append(posTile)

  for level in range(1, height - 1):
    for posTile in createInnerRow(width, level):
      positionTileList.append(posTile)

  for posTile in createTopRow(width, height):
    positionTileList.append(posTile)

  return positionTileList

simpleBoard = Board(createBoard(5, 5))

twoTileBoard = Board(createBoard(1, 2))

mediumBoard = Board(createBoard(10,15))