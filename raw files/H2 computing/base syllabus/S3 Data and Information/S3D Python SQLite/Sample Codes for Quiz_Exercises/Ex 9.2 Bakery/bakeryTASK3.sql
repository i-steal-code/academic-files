SELECT p.ProductCode, p.Name, p.Location, p.Price, Cake.ServingSize
FROM Product p
INNER JOIN Cake 
ON p.ProductCode = Cake.ProductCode AND Cake.Shape="Circle"