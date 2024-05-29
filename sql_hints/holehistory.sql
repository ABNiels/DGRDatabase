SELECT
	p.Name, s.Strokes, l.HoleID
FROM
	Players p
	JOIN Scores s ON s.PlayerID = p.ID
	JOIN Layouts l on l.ID = s.LayoutID
WHERE
	l.layout = 2 AND
	p.Name = 'Micaela'
order by
	l.HoleID asc;