import pandas as pd
from sqlalchemy import create_engine

# Database connection using SQLAlchemy
DATABASE_URL = "mssql+pyodbc://localhost/instnwnd?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(DATABASE_URL)

# Mapping of tables and their columns
TABLE_COLUMN_MAPPING = {
    "Employees": [
        "EmployeeID", "LastName", "FirstName", "Title", "TitleOfCourtesy", "BirthDate", "HireDate", "Address",
        "City", "Region", "PostalCode", "Country", "HomePhone", "Extension", "Photo", "Notes", "ReportsTo", "PhotoPath"
    ],
    "Categories": ["CategoryID", "CategoryName", "Description", "Picture"],
    "Customers": [
        "CustomerID", "CompanyName", "ContactName", "ContactTitle", "Address", "City", "Region", "PostalCode",
        "Country", "Phone", "Fax"
    ],
    "Orders": [
        "OrderID", "CustomerID", "EmployeeID", "OrderDate", "RequiredDate", "ShippedDate", "ShipVia", "Freight",
        "ShipName", "ShipAddress", "ShipCity", "ShipRegion", "ShipPostalCode", "ShipCountry"
    ],
    "Products": [
        "ProductID", "ProductName", "SupplierID", "CategoryID", "QuantityPerUnit", "UnitPrice", "UnitsInStock",
        "UnitsOnOrder", "ReorderLevel", "Discontinued"
    ],
    "Shippers": ["ShipperID", "CompanyName", "Phone"],
    "Suppliers": [
        "SupplierID", "CompanyName", "ContactName", "ContactTitle", "Address", "City", "Region", "PostalCode",
        "Country", "Phone", "Fax", "HomePage"
    ],
    "Order Details": ["OrderID", "ProductID", "UnitPrice", "Quantity", "Discount"],  # Table with space
    "Region": ["RegionID", "RegionDescription"],
    "Territories": ["TerritoryID", "TerritoryDescription", "RegionID"],
    "EmployeeTerritories": ["EmployeeID", "TerritoryID"]
}

# Output Excel file
excel_filename = "database_export.xlsx"

# Create an Excel writer object
with pd.ExcelWriter(excel_filename, engine="xlsxwriter") as writer:
    for table, columns in TABLE_COLUMN_MAPPING.items():
        try:
            table_name = f"[{table}]" if " " in table else table  # Handle spaces in table names
            query = f"SELECT {', '.join(columns)} FROM {table_name}"
            df = pd.read_sql(query, engine)  # Use SQLAlchemy connection
            df.to_excel(writer, sheet_name=table.replace(" ", "_"), index=False)  # Replace spaces in sheet names
            print(f"Exported table: {table}")
        except Exception as e:
            print(f"❌ Error exporting table {table}: {e}")

print(f"✅ Data exported successfully to {excel_filename}")
