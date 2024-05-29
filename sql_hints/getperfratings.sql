SELECT
	p.name, c.name,
	AVG(s.Score)*800.0-400.0+AVG(s.HoleRating) as PerfRating, AVG(s.HoleRating), s.PlayerRating, (AVG(s.Score)*800.0-400.0+AVG(s.HoleRating)) - s.PlayerRating as RelPerformance,
	SUM(h.distance)/285.0 + 30.0 as EstimateSSA, sum(s.strokes), 1000.0+8.5*(SUM(h.distance)/285.0 + (-20.0+50.0/18.0*COUNT(*)) - SUM(s.Strokes)) as EstimatePDGARating
FROM
	Scores s
	JOIN Players p on p.ID = s.PlayerID
	JOIN Layouts l on l.id = s.LayoutID
	JOIN Holes h on h.ID = l.HoleID
	Join Courses c on c.ID = h.CourseID
				
			
WHERE
	NOT s.CardNumber = 0

GROUP BY s.RoundNumber
ORDER BY s.Date ASC
