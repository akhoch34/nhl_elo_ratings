import math
from bs4 import BeautifulSoup
import urllib
import datetime
import operator




ELO = {'Anaheim Ducks':1532,
               'Arizona Coyotes':1468,
               'Boston Bruins':1503,
               'Buffalo Sabres':1468,
               'Calgary Flames':1467,
               'Carolina Hurricanes':1466,
               'Chicago Blackhawks':1529,
               'Colorado Avalanche':1486,
               'Columbus Blue Jackets':1467,
               'Dallas Stars':1544,
               'Detroit Red Wings':1499,
               'Edmonton Oilers':1441,
               'Florida Panthers':1529,
               'Los Angeles Kings':1530,
               'Minnesota Wild':1483,
               'Montreal Canadiens':1481,
               'Nashville Predators':1502,
               'New Jersey Devils':1483,
               'New York Islanders':1524,
               'New York Rangers':1529,
               'Philadelphia Flyers':1508,
               'Pittsburgh Penguins':1552,
               'Ottawa Senators':1484,
               'San Jose Sharks':1528,
               'St. Louis Blues':1554,
               'Tampa Bay Lightning':1526,
               'Toronto Maple Leafs':1436,
               'Vancouver Canucks':1445,
               'Washington Capitals':1567,
               'Winnipeg Jets':1469}

correct_wp = []
incorrect_wp = []
goal_diff = []
elo_diffSet = []


def calcK(margin = 1):
    # if margin > 1:
    #     return 8 * math.log(1+margin)
    # else:
    return 8
correct = 0
incorrect = 0

site = urllib.urlopen('http://www.hockey-reference.com/leagues/NHL_2017_games.html').read()
soup = BeautifulSoup(site)

table = soup.find('table')
table_body = table.find('tbody')
games = table_body.findAll('tr')
start_date = datetime.datetime.strptime("2016-12-1", "%Y-%m-%d")
for game in games:
    dateRow = game.findAll('th')
    cols = game.findAll('td')
    date = str(dateRow[0].text).strip()  # Get Date of Game
    date = datetime.datetime.strptime(date, "%Y-%m-%d")  # Convert string to DateTime
    home = str(cols[2].text).strip() # Get Home Team
    visitor = str(cols[0].text).strip() # Get Visitor Team
    #Calculate Elo Differential
    elo_diff = ELO[home] - ELO[visitor]
    prob_h = round(1.0/(1.0 + math.pow(10, -1*elo_diff/400)), 4) #Calculate the Probability of the home team winning
    prob_v = 1 - prob_h
    if date.date() < datetime.date.today(): # Game has been played, Update Elo Ratings
        visitor_goals = int(str(cols[1].text).strip()) # Get Visitor Score
        home_goals = int(str(cols[3].text).strip()) # Get Home Score
        mov = abs(home_goals - visitor_goals)
        if home_goals > visitor_goals: #Home Wins
            if date.date() > start_date.date():# and (prob_h > 0.60 or prob_v > 0.60):
                if prob_h > prob_v:
                    correct_wp.append(prob_h)
                    correct += 1
                else:
                    incorrect += 1
                    incorrect_wp.append(prob_v)
            wFactor = round(calcK(mov) * prob_v)
            ELO[home] += wFactor
            ELO[visitor] -= wFactor
        else: #Visitor Wins
            if date.date() > start_date.date():# and (prob_h > 0.60 or prob_v > 0.60):
                if prob_h < prob_v:
                    correct_wp.append(prob_v)
                    correct += 1
                else:
                    incorrect_wp.append(prob_h)
                    incorrect += 1
            wFactor = round(calcK(mov) * prob_h)
            ELO[home] -= wFactor
            ELO[visitor] += wFactor



    elif date.date() == datetime.date.today(): # Game is being played today (predict outcome)
        if prob_h > prob_v:
            print home + " have a " + str(100*prob_h) + "% chance of beating the " + visitor
        elif prob_v > prob_h:
            print "The visiting " + visitor + " have a " + str(100*prob_v) + "% chance of beating the " + home
        else:
            print "No favorite in the game between the " + home + " and the " + visitor

total = float(correct + incorrect)


print "\n\nModel is correct " + str(100*(correct/total)) +"% of the time"

sorted_elo = sorted(ELO.items(), key = operator.itemgetter(1), reverse=True)
print "\n\nCurrent Rankings: " + str(sorted_elo)


