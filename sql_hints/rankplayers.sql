WITH RankedScores AS (
    SELECT
        PlayerID,
        PlayerRating,
        Date,
        ROW_NUMBER() OVER (PARTITION BY PlayerID ORDER BY Date DESC, LayoutID DESC) AS rn
    FROM scores
)
SELECT PlayerID, PlayerRating
FROM RankedScores
WHERE rn = 1;
