SELECT competitor.name, scores.score
FROM competitor INNER JOIN scores ON competitor.id = scores.id
WHERE scores.round = ?
ORDER BY scores.score DESC