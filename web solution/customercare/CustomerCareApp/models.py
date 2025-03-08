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
            "EmployeeTerritories"
        ]

        if table_name in valid_tables:
            # If table name contains spaces, we bracket it for SQL Server or quote it if needed
            bracketed_table_name = f"[{table_name}]" if " " in table_name else table_name

            with connection.cursor() as cursor:
                # 1) Get all rows
                query = f"SELECT * FROM {bracketed_table_name}"
                cursor.execute(query)
                table_data = cursor.fetchall()

            with connection.cursor() as cursor:
                # 2) Get column names
                # Here we *can* use parameter substitution for the string value in the WHERE clause
                query = """
                    SELECT COLUMN_NAME
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_NAME = %s
                    ORDER BY ORDINAL_POSITION
                """
                cursor.execute(query, [table_name])
                # This returns a list of tuples like [('EmployeeID',), ('LastName',), ...]
                column_rows = cursor.fetchall()
                coloumn_names = [row[0] for row in column_rows]

            return coloumn_names, table_data
        else:
            # Table name not in the allowed list
            print(f"Invalid table name: {table_name}")
            return [], []
    except Exception as e:
        print(f"models.py view_database error :: {e}")
        return [], []
