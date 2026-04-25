--  IPL Performance Analysis — SQL Analysis Queries
--  Dataset  : matches.csv and deliveries.csv
--  Database : MySQL 8.0

-- 1. Total matches played per season
SELECT season, COUNT(*) AS total_matches
FROM matches
GROUP BY season
ORDER BY season;

-- 2. Most successful teams
SELECT winner AS team, COUNT(*) AS total_wins
FROM matches
WHERE result = 'normal'
GROUP BY winner
ORDER BY total_wins DESC
LIMIT 10;

-- 3. Toss impact on winning
SELECT
    COUNT(*) AS total_matches,
    SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) AS toss_winner_won,
    ROUND(SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2)
        AS toss_win_percentage
FROM matches
WHERE result = 'normal';

-- 4. Top 10 run scorers
SELECT batsman, SUM(batsman_runs) AS total_runs
FROM deliveries
GROUP BY batsman
ORDER BY total_runs DESC
LIMIT 10;

-- 5. Top 10 wicket takers (excluding run outs)
SELECT bowler, COUNT(*) AS total_wickets
FROM deliveries
WHERE dismissal_kind IS NOT NULL
  AND dismissal_kind NOT IN ('run out', 'retired hurt', 'obstructing the field')
GROUP BY bowler
ORDER BY total_wickets DESC
LIMIT 10;

-- 6. Top scoring venues
SELECT venue, SUM(total_runs) AS total_runs
FROM deliveries
JOIN matches ON deliveries.match_id = matches.id
GROUP BY venue
ORDER BY total_runs DESC
LIMIT 10;

-- 7. Win by runs vs win by wickets count
SELECT win_by_runs > 0 AS won_by_runs, COUNT(*) AS total
FROM matches
WHERE result = 'normal'
GROUP BY won_by_runs;