import requests
from bs4 import BeautifulSoup
import numpy as np
import csv

def PlayerStats(stats, player, ncaa, advanced=False):
    if stats == None:
        return
    if ncaa and not advanced:
        player.playerStats.append("NCAA")
    if not ncaa and not advanced:
        player.playerStats.append("INTERNATIONAL")
    for index, stat in enumerate(stats):
        if advanced:
            if ncaa:
                if index < 9:
                    continue
            if not ncaa:
                if index < 11:
                    continue
        if not hasattr(stat, "text"):
            continue
        if stat.text == '\n':
            continue
        if str.isdecimal(stat.text):
            player.playerStats.append(float(stat.text))
        else:
            player.playerStats.append(stat.text)
        # if i == 3:
        #     player.background = stat.text
        # elif i == 17:
        #     player.fieldgoalp = float(stat.text)
        # elif i == 23:
        #     player.threeptp = float(stat.text)
        # elif i == 29:
        #     player.freethrowp = float(stat.text)
        # elif i == 31:
        #     player.offreb = float(stat.text)
        # elif i ==33:
        #     player.defreb = float(stat.text)
        # elif i ==37:
        #     player.assists = float(stat.text)
        # elif i == 39:
        #     player.steals = float(stat.text)
        # elif i == 41:
        #     player.blocks = float(stat.text)
        # elif i == 43:
        #     player.fouls = float(stat.text)
        # elif i == 45:
        #     player.tover = float(stat.text)
        # elif i == 47:
        #     player.ppg = float(stat.text)
        # else:
        #     continue

def GLeaguePlayerStats(stats, player, advanced):
    if stats == None:
        return
    if not advanced:
        player.playerStats.append("GLEAGUE")
    for index, stat in enumerate(stats):
        if advanced:
            if index < 9:
                continue
        if index == 4:
            player.playerStats.append("None")
        if not hasattr(stat, "text"):
            continue
        if stat.text == '\n':
            continue
        if str.isdecimal(stat.text):
            player.playerStats.append(float(stat.text))
        else:
            player.playerStats.append(stat.text)
        # if i == 15:
        #     player.fieldgoalp = float(stat.text)
        # elif i == 21:
        #     player.threeptp = float(stat.text)
        # elif i == 27:
        #     player.freethrowp = float(stat.text)
        # elif i == 29:
        #     player.offreb = float(stat.text)
        # elif i ==31:
        #     player.defreb = float(stat.text)
        # elif i ==35:
        #     player.assists = float(stat.text)
        # elif i == 37:
        #     player.steals = float(stat.text)
        # elif i == 39:
        #     player.blocks = float(stat.text)
        # elif i == 41:
        #     player.fouls = float(stat.text)
        # elif i == 43:
        #     player.tover = float(stat.text)
        # elif i == 45:
        #     player.ppg = float(stat.text)
        # else:
        #     continue


def drafted(pi, player):
    path = None
    for index, info in enumerate(pi):
        if index == 1:
            # In this column is a link to the players personal page with
            # their college stats.
            href = info.find('a')
            path = href.get('href')
        if info.text == '\n':
            continue
        player.playerStats.append(info.text)
        
    return path
        # # Only saving data for columns we care about
        # if index == 1:
        #     # In this column is a link to the players personal page with
        #     # their college stats.
        #     href = info.find('a')
        #     path = href.get('href')
        # elif index == 4:
        #     player.pos = info.text
        # elif index == 5:
        #     player.height = info.text
        # elif index == 6:
        #     player.weight = info.text
        # elif index == 7:
        #     player.age = int(info.text)
        # elif index == 11:
        #     player.nation = info.text
        # else:
        #     continue
    # return path


def undrafted(pi, player):
    player.playerStats.append(61)
    path = None
    for index, info in enumerate(pi):
        if index == 0:
            # In this column is a link to the players personal page with
            # their college stats.
            href = info.find('a')
            path = href.get('href')
        if index == 1:
            player.playerStats.append("None")
            player.playerStats.append("None")
        if info.text == '\n':
            continue
        player.playerStats.append(info.text)
        
        # elif index == 1:
        #     player.pos = info.text
        # elif index == 2:
        #     player.height = info.text
        # elif index == 3:
        #     player.weight = info.text
        # elif index == 4:
        #     player.age = int(info.text)
        # elif index == 8:
        #     player.nation = info.text
        # else:
        #     continue
    return path


class Player:
    def __init__(self):
        self.playerStats = []

    def toArray(self):
        return self.playerStats


year = 11
base_url = "https://basketball.realgm.com"
all_players_url = "https://basketball.realgm.com/nba/draft/past-drafts"
allPlayers = []

# This for loop goes through the last number of years in range
for _ in range(1):
    url = all_players_url + "/20" + str(year) + "?f=i"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    tables = soup.find_all("table", class_="tablesaw")
    # This goes through the tables of 1st round, 2nd round, and undrafted players
    for table in tables:
        tbody = table.find("tbody")
        players = tbody.find_all("tr")
        # This loop goes through each person in the table
        for person in players:
            playerPath = None
            player = Player()
            pi = person.find_all("td")
            # This loop goes through the persons personal info
            if pi[0].text.isnumeric():
                playerPath = drafted(pi, player)
            else:
                playerPath = undrafted(pi, player)

            # Getting the players personal page
            playerURL = base_url + playerPath
            playerPage = requests.get(playerURL)
            playerSoup = BeautifulSoup(playerPage.content, "html.parser")
            # Finding the header for the NCAA per game stats
            ncaa = True
            gleague = False
            international = False
            ncaaHeader = playerSoup.find("h2", string="NCAA Season Stats - Per Game")
            # If not NCAA check if G-League
            if ncaaHeader == None:
                ncaa = False
                ncaaHeader = playerSoup.find(
                    "h2", string="G League Regular Season Stats - Per Game"
                )
                gleague = True
            # If not G-League check if international
            if ncaaHeader == None:
                gleague = False
                ncaaHeader = playerSoup.find(
                    "h2", string="International Regular Season Stats - Per Game"
                )
                international = True
 
            if ncaaHeader == None:
                continue
            # Getting to the table right under the header
            ncaaTable = ncaaHeader.next_element.next_element
            stats = None
            # Getting the ncaa career averages row
            if international:
                ncaaCareer = ncaaTable.find('tbody')
                for row in range(len(ncaaCareer)-1, -1, -1):
                    stuff = ncaaCareer.contents[row]
                    if stuff == '\n':
                        continue
                    inter_year = stuff.contents[1].text
                    if str(year) in inter_year:
                        stats = stuff
                        team = stuff.contents[3]
                        if "All Teams" in team.text:
                            break
                if stats == None:
                    stats = ncaaCareer.contents[len(ncaaCareer) - 1]

            else:
                ncaaCareer = ncaaTable.find('tfoot')
                stats = ncaaCareer.find('tr')

            if ncaa or international:
                PlayerStats(stats, player,ncaa)
                statsAdvanced = None
                if ncaa:
                    ncaaAdvancedHeader = playerSoup.find('h2', string="NCAA Season Stats - Advanced Stats")
                    ncaaAdvancedTable = ncaaAdvancedHeader.next_element.next_element
                    ncaaAdvancedCareer = ncaaAdvancedTable.find('tfoot')
                    statsAdvanced = ncaaAdvancedCareer.find('tr')
                    PlayerStats(statsAdvanced, player, True, True)
                if international:
                    interAdvancedHeader = playerSoup.find('h2', string="International Regular Season Stats - Advanced Stats")
                    interAdvancedTable = interAdvancedHeader.next_element.next_element

                    interAdvancedCareer = interAdvancedTable.find('tbody')
                    for row in range(len(interAdvancedCareer)-1, -1, -1):
                        stuff = interAdvancedCareer.contents[row]
                        if stuff == '\n':
                            continue
                        inter_year = stuff.contents[1].text
                        if str(year) in inter_year:
                            statsAdvanced = stuff
                            team = stuff.contents[3]
                            if "All Teams" in team.text:
                                break
                    PlayerStats(statsAdvanced, player, False, True)

            elif gleague:
                GLeaguePlayerStats(stats, player, False)
                glAdvancedHeader = playerSoup.find('h2', string="G League Regular Season Stats - Advanced Stats")
                glAdvancedTable = glAdvancedHeader.next_element.next_element
                glAdvancedCareer = glAdvancedTable.find('tfoot')
                statsAdvanced = glAdvancedCareer.find('tr')
                GLeaguePlayerStats(statsAdvanced, player, True)



            # Add player to list of all players
            allPlayers.append(player) 
    # Decrement year to go to the previous year's draft when we build the url   
    # year -= 1

playerRows = [instance.playerStats for instance in allPlayers]
# Get number of instances. Used for reshaping
file = open(r'/home/kevin/school/Fall2021/cs472/group-project/venvironment/data-gathering/allPlayers' + str(year) + '.csv', 'w+', newline='')
with file:
    write = csv.writer(file)
    write.writerow(["Pick","Name","Team","Draft-Trades","Pos","HT","WT","Age","YOS","Pre-Draft Team","Class","Nationality",
    "League","Season","School","Class","GP","GS","MIN","FGM","FGA","FG%","3PM","3PA","3P%","FTM","FTA","FT%","OFF","DEF","TRB",
    "AST","STL","BLK","PF","TOV","PTS","TS%","eFG%","ORB%","DRB%","TRB%","AST%","TOV%","STL%",
    "BLK%","USG%","Total S %","PPR","PPS","ORtg","DRtg","PER"])
    write.writerows(playerRows)
file.close()
