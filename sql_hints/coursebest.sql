SELECT
	p.Name, MIN(s.Strokes), l.HoleID
FROM
	Players p
	JOIN Scores s ON s.PlayerID = p.ID
	JOIN Layouts l on l.ID = s.LayoutID
WHERE
	l.HoleID between 19 AND 36 AND
	p.Name = 'Micaela'
group by
 l.HoleID, p.ID;
