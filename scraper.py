from bs4 import BeautifulSoup as bs
import requests, re, time

#   The getGames() function in this module returns a list of dictionaries based on all current scratcher games on https://valottery.com
#   Each dictionary is a game with the following attributes:
#       'title'        : Title of the game, e.g '50X THE MONEY'
#       'id'           : id of the game, e.g '#1965'
#       'overall_odds' : 1 in X odds of the game, e.g 3.05
#       'price'        : price of the ticket in $, e.g 20
#       'num_tickets'  : number of tickets printed, e.g 5678900
#       'prizes'       : a list of dictionaries
#           Each dictionary is a prize with the following attributes:
#               'prize_amount'  : dollar amount of prize, e.g 100
#               'prizes_start'  : how many prizes were available at the beginning, e.g 20000
#               'prizes_current : how many prizes are currently available, e.g 10000


def getSoup(url):
    res = requests.get(url)
    try:
        res.raise_for_status()
    except requests.HTTPError as e:
        print(url, 'responded with', e)
    return bs(res.text, 'html.parser')

def getGameUrls(): # returns a list of url for each scratcher game
    soup = getSoup('https://www.valottery.com/sitemap.xml')
    elems = soup.find_all('loc', string=re.compile("scratcher-games"))
    elems = [elem.get_text() for elem in elems]
    return elems

def getGameDetails(url): # returns a dict with game details from specified url
    game = {}
    soup = getSoup(url)
    ticket_price_display = soup.find(class_='ticket-price-display')
    if ticket_price_display is None:
        return
    game['price'] = int(ticket_price_display.get_text().replace('$',''))
    if game['price'] == 0:
        return None
    title_display = soup.find(class_='title-display')
    game['title'] = title_display.get_text().split('   ')[0] 
    game['id'] = title_display.find('small').get_text()
    odds_display = soup.find(class_='odds-display')
    odds_spans = odds_display.find_all('span')
    game['overall_odds'] = float(odds_spans[0].get_text())
    top_prize_odds = int(odds_spans[1].get_text().replace(',',''))
    prize_table = soup.find('tbody')
    prize_table = prize_table.find_all('td')
    prize_table = [row.get_text().strip() for row in prize_table]
    prize_table = [re.sub('[^0-9]', '', row) for row in prize_table]
    prizes = []
    game['num_tickets'] = top_prize_odds * int(prize_table[1])
    while len(prize_table) > 0:
        prize = {
            'prize_amount'   : int(prize_table[0]),
            'prizes_start'   : int(prize_table[1]),
            'prizes_current' : int(prize_table[2])
        }
        prizes.append(prize)
        for i in range(0, 3):
            prize_table.pop(0)
    game['prizes'] = prizes
    return game

def getGames():
    urls = getGameUrls()
    games = []
    i = 0
    j = len(urls)
    for url in urls:
        try:
            game = getGameDetails(url)
            if game is not None:
                games.append(game)
                print(game['id'])
            print(i, 'of', j)
            i += 1
        except ValueError as e:
            print(e)
    return games