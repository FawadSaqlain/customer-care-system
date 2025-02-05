USE instnwnd
SELECT
    p.ProductID,
    p.ProductName,
    p.UnitPrice
FROM
    Products p
ORDER BY
    p.UnitPrice DESC
