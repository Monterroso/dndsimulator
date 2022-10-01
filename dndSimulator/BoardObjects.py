from .Board import Board
from .Position import Position
from .TileObjects import BottomLeftTile, BottomRightTile, BottomTile, InnerTile, LeftTile, RightTile, TopLeftTile, TopRightTile, TopTile


def createBotRow(width):
    first, *inner, last = [Position(0, 0), *[Position(i, 0) for i in range(1, width - 1)], Position(width - 1, 0)]

    return [(first, BottomLeftTile), *[(ins, BottomTile) for ins in inner], (last, BottomRightTile)]

def createTopRow(width, height):
    first, *inner, last = [Position(0, height - 1), *[Position(i, height - 1) for i in range(1, width - 1)], Position(width - 1, height - 1)]

    return [(first, LeftTile), *[(ins, InnerTile) for ins in inner], (last, RightTile)]

def createInnerRow(width, level):
    first, *inner, last = [Position(0, level), *[Position(i, level) for i in range(1, width - 1)], Position(width - 1, level)]

    return [(first, TopLeftTile), *[(ins, TopTile) for ins in inner], (last, TopRightTile)]


def createBoard(width, height):
    if width <= 3 or height <= 3:
        raise NotImplementedError("A board less than 3 by 3 has not been implemented yet")

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