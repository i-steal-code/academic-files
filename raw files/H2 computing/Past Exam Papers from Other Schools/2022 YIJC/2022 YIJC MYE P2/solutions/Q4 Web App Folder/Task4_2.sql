SELECT ProductName, Buy.Qty, Product.UnitCost FROM Product, Buy
WHERE Buy.SchoolCode = 7612
AND Product.ProductID = Buy.ProductID

SELECT SUM(Buy.Qty* Product.UnitCost) FROM Product, Buy
WHERE Buy.SchoolCode = 7612
AND Product.ProductID = Buy.ProductID