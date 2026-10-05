SELECT competitor.name, AVG(scores.score)
FROM competitor INNER JOIN scores ON competitor.id = scores.id
GROUP BY competitor.name 
ORDER BY competitor.name ASC