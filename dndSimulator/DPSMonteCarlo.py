from random import random
import re
import sys

from dndsimulator.Conditions import SURPRISED

def rollForumla(formula, crit):
  return sum([diceRoller(token, crit) for token in formula.split(" ")])

def diceRoller(formula, crit):
  # Formula in the form of #d#, with number rolled
  dieMatch = re.match("([\+\-]?)([0-9]+)d([0-9]+)p?([0-9]*)", formula)
  if dieMatch != None:
    diceRolled = int(dieMatch.group(2))
    diceSize = int(dieMatch.group(3))
    negative = -1 if dieMatch.group(1) == "-" else 1
    
    critMod = 1 if not crit else 2
    rolls = [((int(random() * diceSize) + 1) * negative) for _ in range(diceRolled * critMod)]
    
    pick = int(dieMatch.group(4))
    
    if pick != None:
      rolls.sort()
      rolls = rolls[pick:]
    
    return sum(rolls)

  return int(formula)


# So what is the thing that will decide as to whether or

# We can create a dictionary for the dps of all of the values, with and without damage
runs = int(sys.argv[1])
formula = sys.argv[2]

nums = [0 for _ in range(21)]

for _ in range(runs):
  nums[rollForumla(formula, False) - 1] += 1
  
  
for index, val in enumerate(nums):
  print("{0}: {1}".format(index, val/runs))
  

