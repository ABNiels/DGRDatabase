SELECT
  s.Date,
  c.name AS courseName,
  l.name AS layoutName,
  COUNT(h.ID) AS numHoles,
  l2.numLayoutHoles as numLayoutHoles,
  s.RoundNumber AS RoundNumber,
  s.CardNumber as CardNumber,
  p.ID as PlayerID,
  p.name as playerName,
  SUM(s.strokes) AS numStrokes,
  SUM(h.par) AS totalPar
FROM Scores s
  JOIN Players p ON p.ID = s.PlayerID
  JOIN Layouts l ON l.id = s.LayoutID
  JOIN Holes h ON h.ID = l.HoleID
  JOIN Courses c ON c.ID = h.CourseID
  LEFT JOIN (
    SELECT
        layout,
        COUNT(h.ID) AS numLayoutHoles
    FROM LAYOUTS l
    JOIN Holes h ON h.ID = l.HoleID
    GROUP BY layout
  ) AS l2 ON l2.layout = l.layout
GROUP BY s.CardNumber, p.ID
ORDER BY s.Date DESC;
