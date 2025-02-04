USE instnwnd
SELECT * from Employees , Categories , Orders , Products , Shippers , Suppliers , Region , Territories , EmployeeTerritories

-- SELECT
--     EmployeeID,
--     LastName,
--     FirstName,
--     Title,
--     TitleOfCourtesy,
--     BirthDate,
--     HireDate,
--     Address,
--     City,
--     Region,
--     PostalCode,
--     Country,
--     HomePhone,
--     Extension,
--     Notes,
--     ReportsTo,
--     Photo
-- FROM
--     Employees
-- WHERE
--     City = 'London' AND Photo IS NULL;

-- line 140 Generated SQL Query: SELECT
--     EmployeeID,
--     LastName,
--     FirstName,
--     Title,
--     TitleOfCourtesy,
--     BirthDate,
--     HireDate,
--     Address,
--     City,
--     Region,
--     PostalCode,
--     Country,
--     HomePhone,
--     Extension,
--     Notes,
--     ReportsTo
-- FROM
--     Employees
-- WHERE
--     City = 'London' AND Photo IS NULL;

SELECT *
FROM Order Details

SELECT
    CASE 
        WHEN EXISTS (SELECT 1 FROM Employees WHERE City = 'London') THEN 'Yes'
        ELSE 'No'
    END AS HasLondonEmployees,
    (SELECT TOP 1 ProductName FROM Products ORDER BY UnitPrice DESC) AS MostExpensiveProduct