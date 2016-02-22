import math
from BeautifulSoup import BeautifulSoup
import urllib
import datetime
import operator


ELO = {'Anaheim Ducks':1500,
               'Arizona Coyotes':1500,
               'Boston Bruins':1500,
               'Buffalo Sabres':1500,
               'Calgary Flames':1500,
               'Carolina Hurricanes':1500,
               'Chicago Blackhawks':1500,
               'Colorado Avalanche':1500,
               'Columbus Blue Jackets':1500,
               'Dallas Stars':1500,
               'Detroit Red Wings':1500,
               'Edmonton Oilers':1500,
               'Florida Panthers':1500,
               'Los Angeles Kings':1500,
               'Minnesota Wild':1500,
               'Montreal Canadiens':1500,
               'Nashville Predators':1500,
               'New Jersey Devils':1500,
               'New York Islanders':1500,
               'New York Rangers':1500,
               'Philadelphia Flyers':1500,
               'Pittsburgh Penguins':1500,
               'Ottawa Senators':1500,
               'San Jose Sharks':1500,
               'St. Louis Blues':1500,
               'Tampa Bay Lightning':1500,
               'Toronto Maple Leafs':1500,
               'Vancouver Canucks':1500,
               'Washington Capitals':1500,
               'Winnipeg Jets':1500}

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

site = urllib.urlopen('http://www.hockey-reference.com/leagues/NHL_2016_games.html').read()
soup = BeautifulSoup(site)

table = soup.find('table')
table_body = table.find('tbody')
games = table_body.findAll('tr')
start_date = datetime.datetime.strptime("2016-1-1", "%Y-%m-%d")
for game in games:
    cols = game.findAll('td')
    date = str(cols[0].text).strip()  # Get Date of Game
    date = datetime.datetime.strptime(date, "%Y-%m-%d")  # Convert string to DateTime
    home = str(cols[3].text).strip() # Get Home Team
    visitor = str(cols[1].text).strip() # Get Visitor Team
    #Calculate Elo Differential
    elo_diff = ELO[home] - ELO[visitor]
    prob_h = round(1.0/(1.0 + math.pow(10, -1*elo_diff/400)), 4) #Calculate the Probability of the home team winning
    prob_v = 1 - prob_h
    if date.date() < datetime.date.today(): # Game has been played, Update Elo Ratings
        visitor_goals = int(str(cols[2].text).strip()) # Get Visitor Score
        home_goals = int(str(cols[4].text).strip()) # Get Home Score
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


