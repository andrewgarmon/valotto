from random import choices
from statistics import median, mean

# The game class takes in a dictionary as returned by the scraper.py module, and constructs a Game Object. 

class Game:
    def __init__(self, gameDict):
        self.title = gameDict['title']
        self.id = gameDict['id']
        self.price = gameDict['price']
        self.num_tickets_total = gameDict['num_tickets']
        self.prizes = gameDict['prizes']
        self.odds = self.getOdds()
        self.num_tickets_claimed = self.getNumTicketsClaimed()
        self.estimated_num_tickets_sold = int(self.num_tickets_claimed / self.odds)
        self.estimated_num_tickets_remaining = self.num_tickets_total - self.estimated_num_tickets_sold
        self.starting_value = self.getStartingValue()
        self.current_value = self.getCurrentValue()
        self.score = self.current_value / self.price
        self.results = []
        self.sims = []
        self.simsMedian = 0

    def setResults(self, results):
        self.results = results

    def getResults(self):
        return self.results

    def printSummary(self):
        print('\nGame:', self.title)
        print('Price:', '$' + str(self.price))
        print('Value:', '$' + str(round(self.current_value, 2)))
        print('Score:', round(self.score, 4))

    def printSimulation(self):
        print('\nGame:', self.title)
        print('Price:', '$' + str(self.price))
        print('Median:', '$' + str(round(self.simsMedian, 2)))
        print('Top 5 Results: ', end='')
        self.sims.sort(reverse=True)
        for sim in self.sims[0:5]:
            print('$' + str(round(sim, 2)), end=' ')
        print('')

    def getStartingValue(self):
        value = 0.0
        for prize in self.prizes:
            prize['starting_odds'] = prize['prizes_start'] / self.num_tickets_total
            prize['starting_value'] = prize['prize_amount'] * prize['starting_odds']
            value += prize['starting_value']
        return value

    def getCurrentValue(self):
        value = 0.0
        for prize in self.prizes:
            prize['current_odds'] = prize['prizes_current'] / self.estimated_num_tickets_remaining
            prize['current_value'] = prize['prize_amount'] * prize['current_odds']
            value += prize['current_value']
        return value

    def getOdds(self):
        total_prizes = 0
        for prize in self.prizes:
            total_prizes += prize['prizes_start']
        return total_prizes / self.num_tickets_total
        
    def getNumTicketsClaimed(self):
        prizes_claimed = 0
        for prize in self.prizes:
            prizes_claimed += (prize['prizes_start'] - prize['prizes_current'])
        return prizes_claimed

    def getPrice(self):
        return self.price

    def getTitle(self):
        return self.title

    def getScore(self):
        return self.score

    def sortByScore(game):
        return game.score

    def sortByMedian(game):
        return game.getSimsMedian() / game.getPrice()

    def getSimsMedian(self):
        return self.simsMedian

    def getSims(self):
        return self.sims

    def playGame(self, money, numSims):
        values = []
        odds = []
        for prize in self.prizes:
            values.append(prize['prize_amount'])
            odds.append(prize['current_odds'])
        values.append(0)
        odds.append(1 - self.getOdds())
        sims = []
        for i in range(0,numSims):
            sims.append(mean(choices(values, weights = odds, k = money // self.getPrice())))
        self.sims = sims
        self.simsMedian = median(sims)
        
