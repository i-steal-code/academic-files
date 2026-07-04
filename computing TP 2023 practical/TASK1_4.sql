SELECT Users.Name
FROM Users INNER JOIN Phasebook ON Users.UserID = Phasebook.UserID
WHERE Users.YearOfRegistration < 2021
ORDER BY desc 