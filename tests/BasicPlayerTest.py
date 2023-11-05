from dndSimulator.GameMaker import SimpleMovementGame
import json

def basicTest():
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
  serializedGame = game.serialize()
  newGame = SimpleMovementGame(data=serializedGame)
  game = newGame
  actorId = game.run()
  game.setAction(actorId, ["move", [(5,5)]])
  serializedGame = game.serialize()
  newGame = SimpleMovementGame(data=serializedGame)
  game = newGame
  actorId = game.run()
  game.setAction(actorId, ["move", [(5,2)]])
  serializedGame = game.serialize()
  newGame = SimpleMovementGame(data=serializedGame)
  game = newGame
  actorId = game.run()
  game.setAction(actorId, ["move", [(4,2)]])
  serializedGame = game.serialize()
  newGame = SimpleMovementGame(data=serializedGame)
  game = newGame
  actorId = game.run()
  game.setAction(actorId, ["move", [(1,2)]])
  serializedGame = game.serialize()
  newGame = SimpleMovementGame(data=serializedGame)
  game = newGame
  actorId = game.run()
  game.setAction(actorId, ["move", [(3,4)]])
  serializedGame = game.serialize()
  newGame = SimpleMovementGame(data=serializedGame)
  game = newGame
  actorId = game.run()

  a = json.dumps(game.serialize())
  
  f = open("output1.json", "w+")
  f.write(a)
  f.close()