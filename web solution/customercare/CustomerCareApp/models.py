
from django.db import connection

def view_database(table_name):
    try:
        # Ensure these match the actual table names in your DB exactly
        valid_tables = [
            "Employees",
            "Categories",
            "Customers",
            "Orders",
            "Products",
            "Shippers",
            "Suppliers",
            "Order Details",   # If your DB table literally has a space
            "Region",
            "Territories",
            "EmployeeTerritories",
            "complaints"
        ]

        if table_name not in valid_tables:
            print(f"models.py: Invalid table name: {table_name}")
            return [], []

        # Debug: List all available tables and their schemas
        with connection.cursor() as cursor:
            cursor.execute("SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES")
            available_tables = cursor.fetchall()
            print("Available tables in DB:", available_tables)

        # Find the matching schema for the given table (case-insensitive)
        matching_schema = None
        for schema, tname in available_tables:
            if tname.lower() == table_name.lower():
                matching_schema = schema
                break

        if matching_schema is None:
            print(f"models.py: No matching table found in database for '{table_name}'")
            return [], []

        # Use the discovered schema to fully qualify the table name.
        # If the table name contains spaces, bracket it.
        if " " in table_name:
            qualified_table = f"{matching_schema}.[{table_name}]"
        else:
            qualified_table = f"{matching_schema}.{table_name}"

        with connection.cursor() as cursor:
            query = f"SELECT * FROM {qualified_table}"
            print(f"models.py line 27: Executing query: {query}")
            cursor.execute(query)
            table_data = cursor.fetchall()

        with connection.cursor() as cursor:
            query = """
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = %s AND TABLE_SCHEMA = %s
                ORDER BY ORDINAL_POSITION
            """
            cursor.execute(query, [table_name, matching_schema])
            column_rows = cursor.fetchall()
            column_names = [row[0] for row in column_rows]

        return column_names, table_data
    except Exception as e:
        print(f"models.py line 50 view_database error :: {e}")
        return [], []

