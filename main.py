from scraper import getGames
from Game import Game
from statistics import median, mean


gameDicts = getGames()
games = []
for gameDict in gameDicts:
    game = Game(gameDict)
    games.append(game)

for game in games:
    print(game.title)
    print('price: $', game.price)
    results = game.playGame(10)
    print('Median: $', median(results))
    print('Results: ', results)
    print('')


# games.sort(key=Game.sort, reverse=True)

# for game in games:
    # game.printSummary()