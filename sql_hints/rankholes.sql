SELECT
	ratingsTable.HoleRating, c.Name, l.Hole, h.Par, AVG(s.Strokes) as AvgStrokes, COUNT(*) as TimesPlayed, h.Distance, h.ID, (AVG(s.Strokes) - h.Par) * 10
FROM
	Holes h
	JOIN Courses c on c.ID = h.CourseID
	JOIN Layouts l ON l.HoleID = h.ID
	JOIN Scores s ON s.LayoutID = l.ID
	JOIN (
    SELECT
		s.ID,
        l.HoleID,
        s.HoleRating,
        s.Date,
        ROW_NUMBER() OVER (PARTITION BY l.HoleID ORDER BY s.Date DESC) AS rn
    FROM Scores s
    JOIN Layouts l ON s.LayoutID = l.ID
) ratingsTable on ratingsTable.ID = s.ID

WHERE
	l.Layout = 2
GROUP BY h.ID
ORDER BY 
	l.Hole ASC