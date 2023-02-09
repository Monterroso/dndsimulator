import math

class Position:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __eq__(self, other):
    return type(other) == type(self) and self.x == other.x and self.y == other.y

  def __hash__(self):
    return hash((self.x, self.y))

  def __add__(self, other):
    return Position(self.x + other.x, self.y + other.y)

  def __sub__(self, other):
    return Position(self.x - other.x, self.y - other.y)
  
  def __repr__(self):
    return "({0}, {1})".format(self.x, self.y)
  
  def max(self, other):
    return Position(max(self.x, other.x), max(self.y, other.y))
  
  def min(self, other):
    return Position(min(self.x, other.x), min(self.y, other.y))
  
  def toDict(self, serializer):
    return {
      "x": serializer(self.x),
      "y": serializer(self.y),
    }
    