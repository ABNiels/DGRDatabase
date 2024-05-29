SELECT
  r.HoleRating
FROM
  Ratings r
  JOIN Scores s on r.ScoreID = s.ID
  JOIN Holes h ON s.HoleID = h.ID
WHERE
  h.Distance = (
    SELECT
      MIN(Distance)
    FROM
      Holes
    WHERE
      Distance >= 320
      AND Par = 3
  )
ORDER BY
  r.Date DESC
LIMIT
  1;