class Action:
  def __init__(self):
    pass
  
  
class MoveAction(Action):
  def __init__(self, mover, origin, destination):
    self.mover = mover
    self.origin = origin
    self.destination = destination

class MultiAttackAction(Action):
  def __init__(self, attacker, attacks):
    self.attacker = attacker,
    self.attacks = attacks