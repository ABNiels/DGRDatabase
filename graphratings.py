from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import sqlite3
import numpy as np

# Make connection and cursor to database
conn = sqlite3.connect('discgolfrewards.db')
cur = conn.cursor()


# Get rating for player
def getPlayerRating(playerID):
    cur.execute(
        "SELECT Date, PlayerRating FROM Scores WHERE PlayerID = ? ORDER BY Date ASC",
        (playerID,)
    )
    return cur.fetchall()

def getHoleRating(holeID):
    cur.execute(
        "SELECT Date, HoleRating FROM Scores JOIN Layouts ON Layouts.ID = Scores.LayoutID WHERE Layouts.HoleID = ? ORDER BY Date ASC, CardNumber ASC",
        (holeID,)
    )
    return cur.fetchall()

def getPlayerHoleRating(playerID, holeID):
    cur.execute(
        "SELECT Date, PlayerHoleRating FROM Scores WHERE PlayerID = ? AND layoutID = ? ORDER BY Date ASC",
        (playerID, holeID)
    )
    return cur.fetchall()

def plotHoleRating(holeIDs):
    for holeID in holeIDs:
        ratings = getHoleRating(holeID)
        ratings = np.array(ratings)
        x = ratings[:,0]
        y = ratings[:,1]
        plt.plot(y)
    plt.show()
def plotPlayerRating(playerIDs):
    for playerID in playerIDs:
        ratings = getPlayerRating(playerID)
        ratings = np.array(ratings)
        x = ratings[:,0]
        y = ratings[:,1]
        plt.plot(y)
    plt.show()

def plotCourseRating(course):
    # 6x3 subplots
    fig, ax = plt.subplots(6,3,sharex='col', sharey='row')
    for i in range(18):
        # Get hole rating and plot it
        ratings = getHoleRating(i+(course*18)+1)
        ratings = np.array(ratings)
        #x = ratings[:,0]
        y = ratings[:,1]
        ax[i//3,i%3].plot(y)
    # Have all y axes have the same scale
    plt.subplots_adjust(wspace=0, hspace=0)


    # Show the plot
    plt.show()

def plotPlayerCourseRating(player, course):
    # 6x3 subplots
    fig, ax = plt.subplots(6,3,sharex='col', sharey='row')
    for i in range(18):
        # Get hole rating and plot it
        ratings = getPlayerHoleRating(player, i+(course*18)+1)
        ratings = np.array(ratings)
        #x = ratings[:,0]
        y = ratings[:,1]
        ax[i//3,i%3].plot(y)
    # Have all y axes have the same scale
    plt.subplots_adjust(wspace=0, hspace=0)


    # Show the plot
    plt.show()

if __name__ == "__main__":
    plotPlayerRating([1,2,28,29])
    #plotHoleRating([32, 34, 24, 36])
    #plotCourseRating(1)
    #plotPlayerCourseRating(1, 0)


# close connection
conn.close()