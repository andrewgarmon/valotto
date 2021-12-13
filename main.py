from scraper import getGames
from Game import Game

gameDicts = getGames()
games = []
for gameDict in gameDicts:
    game = Game(gameDict)
    games.append(game)

games.sort(key=Game.sort, reverse=True)

for game in games:
    game.printSummary()