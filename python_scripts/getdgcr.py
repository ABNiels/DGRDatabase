# Get html and parse it with lxml
import requests
from lxml import html

# connect to the database
import sqlite3
conn = sqlite3.connect('discgolfrewards.db')
db = conn.cursor()

from datetime import datetime, timedelta

def date_to_mjd(date_string):
    date_format = "%Y-%m-%dT%H:%M:%S%z"
    
    # Parse the input date string
    date_obj = datetime.strptime(date_string, date_format)
    
    # Convert the datetime object to offset-naive
    offset_naive_date_obj = date_obj.replace(tzinfo=None)
    
    # Calculate the Modified Julian Date (MJD)
    mjd_epoch = datetime(1858, 11, 17)  # MJD epoch
    mjd = (offset_naive_date_obj - mjd_epoch).total_seconds() / 86400.0
    
    return mjd

# get user playerID
def get_playerID(player):
    db.execute("SELECT ID FROM players WHERE name = ?", (player,))
    # if the player is not in the database, add it
    playerID = db.fetchone()
    if playerID is None:
        db.execute("INSERT INTO players (name) VALUES (?)", (player,))
        conn.commit()
        # get the playerID
        return get_playerID(player)
    return playerID[0]

def insert_score(playerID, date, hole, score):
    db.execute("INSERT INTO scores (playerID, date, layoutID, strokes, roundNumber, CardNumber) VALUES (?, ?, ?, ?, 0, 0)", (playerID, date, hole, score))
    conn.commit()
# Get the html
url = 'https://www.dgcoursereview.com/courses/rockwell-park.8437/rounds?page=1'
response = requests.get(url)

# Parse the html
tree = html.fromstring(response.content)

HOLE = 0
DISTANCE = 1
PAR = 2
SCORE = 3

DATE = 0

# Get the rounds
rounds = tree.xpath('//table')
players = tree.xpath('//span[contains(@class, "c_name")]')

for roundInfo, holeInfo, player in zip(rounds[::2], rounds[1::2], players):
    player = player.text
    # Get the trs in the body where the class is not _last_totals
    date = roundInfo.xpath('.//time/@datetime')[0]
    date = int(date_to_mjd(date))
    playerID = get_playerID(player)
    print(playerID, int(date))
    holes = holeInfo.xpath('.//tbody/tr[not(contains(@class, "_totals"))]')
    for hole in holes:
        # Get 4th column
        info = hole.xpath('.//td')
        print(info[HOLE].text, info[SCORE].text)
        insert_score(playerID, date, int(info[HOLE].text)+18, info[SCORE].text)


# close connection
conn.close()