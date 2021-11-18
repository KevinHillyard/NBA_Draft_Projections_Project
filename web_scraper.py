import requests
from bs4 import BeautifulSoup
import numpy as np
import csv


def PlayerStats(stats, player):
    for i, stat in enumerate(stats):
        if i == 3:
            player.background = stat.text
        elif i == 17:
            player.fieldgoalp = float(stat.text)
        elif i == 23:
            player.threeptp = float(stat.text)
        elif i == 29:
            player.freethrowp = float(stat.text)
        elif i == 31:
            player.offreb = float(stat.text)
        elif i == 33:
            player.defreb = float(stat.text)
        elif i == 37:
            player.assists = float(stat.text)
        elif i == 39:
            player.steals = float(stat.text)
        elif i == 41:
            player.blocks = float(stat.text)
        elif i == 43:
            player.fouls = float(stat.text)
        elif i == 45:
            player.tover = float(stat.text)
        elif i == 47:
            player.ppg = float(stat.text)
        else:
            continue


def GLeaguePlayerStats(stats, player):
    player.background = "GLEAGUE"
    for i, stat in enumerate(stats):
        if i == 15:
            player.fieldgoalp = float(stat.text)
        elif i == 21:
            player.threeptp = float(stat.text)
        elif i == 27:
            player.freethrowp = float(stat.text)
        elif i == 29:
            player.offreb = float(stat.text)
        elif i == 31:
            player.defreb = float(stat.text)
        elif i == 35:
            player.assists = float(stat.text)
        elif i == 37:
            player.steals = float(stat.text)
        elif i == 39:
            player.blocks = float(stat.text)
        elif i == 41:
            player.fouls = float(stat.text)
        elif i == 43:
            player.tover = float(stat.text)
        elif i == 45:
            player.ppg = float(stat.text)
        else:
            continue


def drafted(pi, player):
    path = None
    for index, info in enumerate(pi):
        # Only saving data for columns we care about
        if index == 0:
            if (int(info.text)) > 60:
                player.draftnum = 61
            else:
                player.draftnum = int(info.text)
        elif index == 1:
            # In this column is a link to the players personal page with
            # their college stats.
            href = info.find("a")
            path = href.get("href")
        elif index == 4:
            player.pos = info.text
        elif index == 5:
            player.height = info.text
        elif index == 6:
            player.weight = info.text
        elif index == 7:
            player.age = int(info.text)
        elif index == 11:
            player.nation = info.text
        else:
            continue
    return path


def undrafted(pi, player):
    player.draftnum = 61
    path = None
    for index, info in enumerate(pi):
        # Only saving data for columns we care about
        if index == 0:
            # In this column is a link to the players personal page with
            # their college stats.
            href = info.find("a")
            path = href.get("href")
        elif index == 1:
            player.pos = info.text
        elif index == 2:
            player.height = info.text
        elif index == 3:
            player.weight = info.text
        elif index == 4:
            player.age = int(info.text)
        elif index == 8:
            player.nation = info.text
        else:
            continue
    return path


class Player:
    def __init__(self):
        self.pos = None
        self.height = None
        self.weight = None
        self.ppg = None
        self.threeptp = None
        self.fieldgoalp = None
        self.freethrowp = None
        self.background = None
        self.steals = None
        self.tover = None
        self.assists = None
        self.offreb = None
        self.defreb = None
        self.blocks = None
        self.fouls = None
        self.draftnum = None
        self.age = None
        self.nation = None

    def toArray(self):
        return [
            self.pos,
            self.height,
            self.weight,
            self.ppg,
            self.threeptp,
            self.fieldgoalp,
            self.freethrowp,
            self.background,
            self.steals,
            self.tover,
            self.assists,
            self.offreb,
            self.defreb,
            self.blocks,
            self.fouls,
            self.age,
            self.nation,
            self.draftnum,
        ]


year = 2021
base_url = "https://basketball.realgm.com"
all_players_url = "https://basketball.realgm.com/nba/draft/past-drafts"
allPlayers = []

# This for loop goes through the last number of years in range
for _ in range(1):
    url = all_players_url + "/" + str(year) + "?f=i"
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

            # Getting to the table right under the header
            ncaaTable = ncaaHeader.next_element.next_element
            # Getting the ncaa career averages row
            if international:
                ncaaCareer = ncaaTable.find("tbody")
            else:
                ncaaCareer = ncaaTable.find("tfoot")
            # The row itself
            stats = ncaaCareer.find("tr")

            if ncaa or international:
                PlayerStats(stats, player)
            elif gleague:
                GLeaguePlayerStats(stats, player)

            # Add player to list of all players
            allPlayers.append(player)
    # Decrement year to go to the previous year's draft when we build the url
    year -= 1

playerRows = [instance.toArray() for instance in allPlayers]
# Get number of instances. Used for reshaping
file = open(r"./allPlayers.csv", "w+", newline="")
with file:
    write = csv.writer(file)
    write.writerow(
        [
            "Position",
            "Height",
            "Weight",
            "PPG",
            "3pt%",
            "FG%",
            "FT%",
            "League",
            "Steals",
            "TOV",
            "Assits",
            "Off-Rebount",
            "Def-Rebound",
            "Blocks",
            "Fouls",
            "Age",
            "Nation",
            "Draft Position",
        ]
    )
    write.writerows(playerRows)
file.close()
