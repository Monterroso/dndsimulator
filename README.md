# DndSimulator

This is a pet project of mine! It's currently a wip. The goal is for the ability to create virtual agents, put them on a virtual board, along with any human players who with to participate, and then have it run and go to town!

We've still got a long way to go before it's got any semblence of actual d&d functionality, but I won't give up (god willing lmao)

## Installation and updating
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dndSimulator like below. 
Rerun this command to check for and install  updates .
```bash
pip install git+https://github.com/Monterroso/dndsimulator
```

## Usage
Features:
GameMaker.SimpleMovementGame --> Used to create and manage a game with simple agents that can move, along with any player agents

#### Demo of some of the features:
```python
from dndSimulator.GameMaker import SimpleMovementGame

actorDatas = [
    ["actor1", "speed1", "basicMovementAI"],
    ["actor2", "speed2", "basicMovementAI"],
    ["actor3", "speed3", "player"],
  ]

  actorTypeDatas = [
    ["speed1", 1],
    ["speed2", 2],
    ["speed3", 3],
  ]

  board = [(5,5)]

  game = SimpleMovementGame(actorDatas, actorTypeDatas, board)
  
  actorId = game.run()
  game.setAction(actorId, ["move", [(2,2)]])
  actorId = game.run()
  game.setAction(actorId, ["move", [(5,5)]])
  actorId = game.run()
  game.setAction(actorId, ["move", [(5,2)]])
  actorId = game.run()
  game.setAction(actorId, ["move", [(4,2)]])
  actorId = game.run()
  game.setAction(actorId, ["move", [(1,2)]])
  actorId = game.run()
  game.setAction(actorId, ["move", [(3,4)]])
  actorId = game.run()
```

## License
[MIT](https://choosealicense.com/licenses/mit/)