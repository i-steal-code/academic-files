SELECT competitor.name, SUM(scores.score), 
CASE WHEN SUM(scores.score) > 250 THEN 'qualified' ELSE 'did not qualify' 
END
FROM competitor INNER JOIN scores ON competitor.id = scores.id
GROUP BY competitor.name 
ORDER BY SUM(scores.score) DESC