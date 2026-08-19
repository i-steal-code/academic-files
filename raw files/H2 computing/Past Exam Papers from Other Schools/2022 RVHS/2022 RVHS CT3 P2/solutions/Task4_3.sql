SELECT MonitorInfo.ModelNo,
Round(Price * Promotion / 100, 2) as "Actual Price",
Resolution,
Count(MonitorInfo.ModelNo) as Quantity
FROM MonitorInfo, ProductInfo, SalesRecord
WHERE MonitorInfo.ModelNo = ProductInfo.ModelNo
AND ProductInfo.SerialNo = SalesRecord.SerialNo
GROUP BY MonitorInfo.ModelNo
ORDER BY Count(MonitorInfo.ModelNo) DESC