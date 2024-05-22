SELECT
	DISTINCT c.Name, l.name, COUNT(l.Hole) as NumHoles, SUM(h.distance) as TotalDistance, LayoutRatings.Rating, SUM(h.distance)/285 + 30 as EstimateSSA, SUM(h.par)
FROM
	Courses c
	JOIN Holes h on h.CourseID = c.ID
	JOIN Layouts l on l.HoleID = h.id
	JOIN (
		SELECT
			AVG(s.HoleRating) as Rating, l.Layout as layout
		FROM
			Scores s
			JOIN Layouts l on s.LayoutID = l.ID
		GROUP BY l.layout
		ORDER BY DATE DESC
	) LayoutRatings on LayoutRatings.layout = l.layout
GROUP BY l.Layout
	