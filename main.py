from scraper import getGames
from Game import Game
from statistics import median, mean
import json, sys
from os.path import exists
from os import remove

if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv) < 2:
    print(''' 
    -h, --help            show this help menu
    -r, --rank            shows ranking of all games
    -s N, --simulate N    simulates with N games
    -u, --update          updates games.txt with latest info
    ''')
    exit()

if '-u' in sys.argv or '--update' in sys.argv:
    remove('games.txt')

if not exists('games.txt'):
    gameDicts = getGames()
    f = open('games.txt', 'a')
    f.write(json.dumps(gameDicts))
    f.close()

f = open('games.txt', 'r')
gameDicts = json.loads(f.read())
games = []
for gameDict in gameDicts:
    game = Game(gameDict)
    games.append(game)

if '-s' in sys.argv or '--simulate' in sys.argv:
    for game in games:
        print(game.title)
        print('price: $', game.price)
        results = game.playGame(10)
        # print('Median: $', median(results))
        print('Results: ', results)
        print('')


if '--rank' in sys.argv or '-r' in sys.argv:
    games.sort(key=Game.sort, reverse=True)
    for game in games:
        game.printSummary()