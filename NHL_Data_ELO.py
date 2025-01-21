import math
from bs4 import BeautifulSoup
import requests
import datetime
import operator

ELO = {
        'Anaheim Ducks': 1418, 
        'Boston Bruins': 1528, 
        'Buffalo Sabres': 1497, 
        'Calgary Flames': 1482, 
        'Carolina Hurricanes': 1565, 
        'Chicago Blackhawks': 1400, 
        'Colorado Avalanche': 1550, 
        'Columbus Blue Jackets': 1430, 
        'Dallas Stars': 1562, 
        'Detroit Red Wings': 1499, 
        'Edmonton Oilers': 1541, 
        'Florida Panthers': 1560, 
        'Los Angeles Kings': 1511, 
        'Minnesota Wild': 1489, 
        'Montreal Canadiens': 1437, 
        'Nashville Predators': 1534, 
        'New Jersey Devils': 1479, 
        'New York Islanders': 1499, 
        'New York Rangers': 1574, 
        'Philadelphia Flyers': 1476, 
        'Pittsburgh Penguins': 1488, 
        'Ottawa Senators': 1484, 
        'San Jose Sharks': 1380, 
        'Seattle Kraken': 1461, 
        'St. Louis Blues': 1509, 
        'Tampa Bay Lightning': 1526, 
        'Toronto Maple Leafs': 1528, 
        'Utah Hockey Club': 1474, 
        'Vancouver Canucks': 1540, 
        'Vegas Golden Knights': 1517, 
        'Washington Capitals': 1502, 
        'Winnipeg Jets': 1560
    }

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

url = 'http://www.hockey-reference.com/leagues/NHL_2025_games.html'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

table = soup.find('table')
table_body = table.find('tbody')
games = table_body.findAll('tr')
evaluation_start_date = datetime.datetime.strptime("2025-1-1", "%Y-%m-%d")
# print(games)
for game in games:
    dateRow = game.findAll('th')
    cols = game.findAll('td')
    date = str(dateRow[0].text).strip()  # Get Date of Game
    date = datetime.datetime.strptime(date, "%Y-%m-%d")  # Convert string to DateTime
    # print(cols)
    home = str(cols[3].text).strip() # Get Home Team
    visitor = str(cols[1].text).strip() # Get Visitor Team
    #Calculate Elo Differential
    if home == '' or visitor == '':
        continue
    # print(home)
    elo_diff = ELO[home] - ELO[visitor]
    prob_h = round(1.0/(1.0 + math.pow(10, -1*elo_diff/400)), 4) #Calculate the Probability of the home team winning
    prob_v = 1 - prob_h
    if date.date() < datetime.date.today(): # Game has been played, Update Elo Ratings
        visitor_goals = int(str(cols[2].text).strip()) # Get Visitor Score
        home_goals = int(str(cols[4].text).strip()) # Get Home Score
        mov = abs(home_goals - visitor_goals)
        if home_goals > visitor_goals: #Home Wins
            if date.date() >= evaluation_start_date.date(): # (prob_h > 0.60 or prob_v > 0.60):
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
            if date.date() >= evaluation_start_date.date(): # (prob_h > 0.60 or prob_v > 0.60):
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
            print(home + " have a " + str(round(100*prob_h,2)) + "% chance of beating the " + visitor)
        elif prob_v > prob_h:
            print("The visiting " + visitor + " have a " + str(round(100*prob_v,2)) + "% chance of beating the " + home)
        else:
            print("No favorite in the game between the " + home + " and the " + visitor)

total = float(correct + incorrect)


print("\n\nModel is correct " + str(round(100*(correct/total),2)) +"% of the time")

sorted_elo = sorted(ELO.items(), key = operator.itemgetter(1), reverse=True)
print("\n\nCurrent Rankings: " + str(sorted_elo))