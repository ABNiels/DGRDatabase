import sqlite3

# Conenct to database: discgolfrewards.db
conn = sqlite3.connect('discgolfrewards.db')
# Create a cursor
cur = conn.cursor()


# LOG(10^0.5,20)
a2 = 0.384310893
a1 = 0.2
a3 = 360
k1 = 35
k2 = 40

defaultPlayerRating = 1000
defaultHoleRating = 1700

"""
    -4: 0.9990,
    -3: 0.9873,
    -2: 0.9335,
    -1: 0.7767,
    0: 0.5459,
    1: 0.3022,
    2: 0.1281,
    3: 0.05338,
    4: 0.02267,
    5: 0.004631,
    6: 0.002437,
    7: 0.0002437,
"""
score_lookup = {
    -2: 0.8224995,
    -1: 0.5593611  ,
    0: 0.4087432  ,
    1: 0.2702973  ,
    2: 0.1835848,
    3: 0.1457385 ,
    #4: 0.3000000,
    #5: 0.1169737 ,
    #6: 0.1000000 ,
    #7: 0.01841748,
}

def calculateScore(par, strokes):
    try:
        return score_lookup[strokes-par]
    except:
        return 0 if strokes > par else 1
    # return 1/(1+pow(20, (strokes-par)*a2))

def calculateRating(playerRating, playerHoleRating, holeRating, score):
    modifiedPlayerRating = playerRating + (playerHoleRating - playerRating)*a1
    print(playerRating, playerHoleRating, holeRating, score, modifiedPlayerRating)
    expectedScore = 1/(1+pow(10, (holeRating-modifiedPlayerRating)/a3))
    if modifiedPlayerRating < 1900:
        k3 = 16*((0.56 + 0.000004*(1900-modifiedPlayerRating)**2)**0.5)
    else:
        k3 = 12
    return (
        playerRating + k3*(score-expectedScore),
        playerHoleRating, # + k1*(score-expectedScore),
        holeRating + k2*(expectedScore-score),
    )
    



def getAllScores():
    cur.execute(
    "SELECT s.PlayerID, l.HoleID, h.par, s.strokes, s.Date, s.ID, l.Hole FROM Scores s JOIN Layouts l ON l.ID = s.LayoutID JOIN Holes h on h.ID = l.HoleID ORDER BY s.Date ASC, l.Hole ASC"
    )
    # return rows
    return cur.fetchall()

def getPlayerRatings(playerID, HoleID, Date, layoutHole):
    fetchedRows = []
    #print(f"playerID: {playerID}, HoleID: {HoleID}, Date: {Date}, layoutHole: {layoutHole}")
    cur.execute(
        "SELECT s.PlayerRating FROM Scores s JOIN Layouts l ON l.ID = s.LayoutID JOIN Holes h on h.ID = l.HoleID WHERE (s.Date < ? OR (s.Date = ? AND l.Hole < ?)) AND s.PlayerID = ? ORDER BY s.Date DESC, l.Hole DESC LIMIT 1",
        (Date, Date, layoutHole, playerID)
    )
    fetchedRows.append(cur.fetchone())
    cur.execute(
        """
        WITH PHRating as (
            SELECT 
                playerID, Score, Date, HoleRating, LayoutID,
                ROW_NUMBER() OVER (PARTITION BY playerID ORDER BY date DESC) AS row_num
            FROM Scores
            WHERE LayoutID = ? AND PlayerID = ? AND Date < ?
        ) 
            SELECT
                AVG(phr.Score)*800.0-400.0+AVG(phr.HoleRating) as PlayerHoleRating
            FROM
                PHRating phr
            WHERE row_num <= 3
            GROUP BY phr.PlayerID
        """,
        (HoleID, playerID, Date)
    )
    fetchedRows.append(cur.fetchone())
    cur.execute(
        "SELECT s.HoleRating FROM Scores s JOIN Layouts l ON l.ID = s.LayoutID JOIN Holes h on h.ID = l.HoleID WHERE s.Date < ? AND l.HoleID = ? ORDER BY s.Date DESC, l.Hole DESC LIMIT 1",
        (Date, HoleID)
    )
    fetchedRows.append(cur.fetchone())

    if fetchedRows[0] is None or fetchedRows[0][0] is None:
        # Get Default Player Rating
        cur.execute(
            "SELECT DefRating from Players where ID = ?",
            (playerID,)
        )
        (val, ) = cur.fetchone()
        if val is not None:
            fetchedRows[0] = val
        else:
            fetchedRows[0] = defaultPlayerRating
    else:
        fetchedRows[0] = fetchedRows[0][0]
    fetchedRows[1] = fetchedRows[0]-50 if fetchedRows[1] is None or fetchedRows[1][0] is None else fetchedRows[1][0]

    if fetchedRows[2] is None or fetchedRows[2][0] is None:
        # Get Default Hole Rating
        cur.execute(
            "SELECT DefRating from Holes where ID = ?",
            (HoleID,)
        )
        (val, ) = cur.fetchone()
        if val is not None:
            fetchedRows[2] = val
        else:
            # Get the closest hole
            cur.execute(
                "SELECT par, distance FROM Holes WHERE ID = ?",
                (HoleID,)
            )
            par, distance = cur.fetchone()
            # Find the closest hole
            cur.execute(
                """
                SELECT
                    s.HoleRating, h.par, h.distance, ABS(h.distance - ?) as DistDiff, l.HoleID
                FROM
                    Scores s
                    JOIN Layouts l ON l.ID = s.LayoutID
                    JOIN Holes h on h.ID = l.HoleID
                WHERE
                    s.Date < ? AND
                    h.Par = ? AND
                    h.ID != ?
                ORDER BY DistDiff ASC, s.Date DESC
                limit 1
                """,
                (distance, Date, par, HoleID)
            )
            try:
                (rating, par, distance, distDiff, otherHoleID) = cur.fetchone()
            except:
                rating = defaultHoleRating
                print("IT messed up")
            print("THIS IS THE RATING THAT WE GOT: ", rating)
            fetchedRows[2] = rating
    else:
        fetchedRows[2] = fetchedRows[2][0]
    return fetchedRows

def setRating(playerRating, playerHoleRating, holeRating, score, ScoreID):
    cur.execute(
        "UPDATE Scores SET PlayerRating = ?, PlayerHoleRating = ?, HoleRating = ?, score = ? WHERE ID = ?",
        (playerRating, playerHoleRating, holeRating, score, ScoreID)
    )
 
i=0
for playerID, HoleID, par, strokes, Date, ScoreID, layoutHole in getAllScores():
  
  print(playerID, HoleID, par, strokes, Date, ScoreID, layoutHole)
  ratings = getPlayerRatings(playerID, HoleID, Date, layoutHole)
  print(ratings)
  score = calculateScore(par, strokes)
  updatedRatings = calculateRating(*ratings, score)
  #print(updatedRatings)
  setRating(*updatedRatings, score, ScoreID)
  i += 1
  if i >= 50:
    pass #break

# Write db and close connection
conn.commit()
conn.close()
print("finished")
