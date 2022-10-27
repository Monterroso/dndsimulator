class EndAfterXRounds:
  def __init__(self, rounds):
    self.rounds = rounds

def __call__(self, game):
  return game.getRoundCount() == self.rounds