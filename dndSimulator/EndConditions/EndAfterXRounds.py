class EndAfterXRounds:
  """Checks if the game has reached the specified round count
  """
  def __init__(self, rounds):
    self.rounds = rounds

  def __call__(self, game):
    return game.getRoundCount() == self.rounds