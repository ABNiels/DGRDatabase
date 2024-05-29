WITH HoleRatings AS (
    SELECT
		l.hole,
        s.HoleRating,
		h.par,
		h.distance,
		s.layoutID,
        ROW_NUMBER() OVER (PARTITION BY l.HoleID ORDER BY s.Date DESC) AS rowNum
    FROM Scores s
    JOIN Layouts l ON s.LayoutID = l.ID
	JOIN Holes h ON l.HoleID = h.ID
	WHERE l.layout = 2
),
PlayerRatings AS (
    SELECT
        PlayerID,
        PlayerRating,
        ROW_NUMBER() OVER (PARTITION BY PlayerID ORDER BY Date DESC, LayoutID DESC) AS rowNum
    FROM scores
),
PHRating AS (
    SELECT 
        playerID, Score, Date, HoleRating, LayoutID,
        ROW_NUMBER() OVER (PARTITION BY playerID, LayoutID ORDER BY date DESC) AS row_num
    FROM Scores
) 
SELECT
	hr.hole,
	hr.HoleRating,
	hr.par,
	hr.distance,
	MAX(CASE WHEN pr.PlayerID = 1 THEN pr.PlayerRating END) AS Player1Rating,
	MAX(CASE WHEN pr.PlayerID = 2 THEN pr.PlayerRating END) AS Player2Rating,
	AVG(CASE WHEN phr.PlayerID = 1 THEN phr.Score ELSE NULL END)*800.0-400.0+AVG(CASE WHEN phr.PlayerID = 1 THEN phr.HoleRating ELSE NULL END) as Player1HoleRating,
	AVG(CASE WHEN phr.PlayerID = 2 THEN phr.Score ELSE NULL END)*800.0-400.0+AVG(CASE WHEN phr.PlayerID = 2 THEN phr.HoleRating ELSE NULL END) as Player2HoleRating,
	
	AVG(CASE WHEN phr.PlayerID = 23 THEN phr.Score ELSE NULL END)*800.0-400.0+AVG(CASE WHEN phr.PlayerID = 23 THEN phr.HoleRating ELSE NULL END) as Player23HoleRating
FROM 
	HoleRatings hr
	JOIN PlayerRatings pr ON hr.rowNum = 1 AND pr.rowNum = 1
	JOIN PHRating phr ON hr.LayoutID = phr.LayoutID AND phr.row_num <= 3
GROUP BY hr.hole, hr.HoleRating, hr.par, hr.distance;
