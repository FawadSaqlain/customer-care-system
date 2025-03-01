
# import google.generativeai as genai
import re
import spacy
import pandas as pd
from sqlalchemy import create_engine
import pyodbc

# Load spaCy's model for Named Entity Recognition (NER)
nlp_spacy = spacy.load("en_core_web_sm")

# Database connection strings
def create_connection():
    try:
        engine = create_engine("mssql+pyodbc://@127.0.0.1,1433/instnwnd?driver=ODBC+Driver+17+for+SQL+Server")
        return engine
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def conn_cursor():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=127.0.0.1,1433;"
        "DATABASE=instnwnd;"
        "Trusted_Connection=yes;"
        "Connection Timeout=60;"
    )
    try:
        conn = pyodbc.connect(conn_str)
        print("Connected to MSSQL Server successfully!")
        return conn
    except Exception as e:
        print(f"Error connecting to MSSQL Server: {e}")
        return None

# Map natural language columns to database schema
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
    "Order Details": ["OrderID", "ProductID", "UnitPrice", "Quantity", "Discount"],
    "Region": ["RegionID", "RegionDescription"],
    "Territories": ["TerritoryID", "TerritoryDescription", "RegionID"],
    "EmployeeTerritories": ["EmployeeID", "TerritoryID"]
}

# Preprocess the natural language query
def preprocess_query(natural_language_query):
    doc = nlp_spacy(natural_language_query)
    for ent in doc.ents:
        if ent.label_ == "GPE":  # Geopolitical entity (city, country)
            natural_language_query = natural_language_query.replace(ent.text, f"'{ent.text}'")
    for table, columns in TABLE_COLUMN_MAPPING.items():
        natural_language_query = re.sub(rf"\b{table}\b", table, natural_language_query, flags=re.IGNORECASE)
        for column in columns:
            natural_language_query = re.sub(rf"\b{column}\b", column, natural_language_query, flags=re.IGNORECASE)
    stopwords = ["list of", "show me", "all the", "who"]
    for word in stopwords:
        natural_language_query = natural_language_query.replace(word, "")
    return natural_language_query.strip()

# Convert natural language to SQL
def nl_to_sql(natural_language_query,model):
    try:
        cleaned_query = preprocess_query(natural_language_query)
        print(f"line 90 Cleaned Query: {cleaned_query}")
        
        # Prompt for the model
        prompt = (
            f"Translate the following natural language question into an SQL query for Microsoft SQL Server. "
            f"Use correct syntax without backticks: {cleaned_query}.\n"
            f"Ensure the query is well-formatted for this database schema: {TABLE_COLUMN_MAPPING}"
        )
        
        # Generate content using the model
        response = model.generate_content(prompt)
        
        # Clean up the response
        sql_query = response.text.strip()
        sql_query = sql_query.replace("`", "")  # Remove any backticks
        # Ensure no unwanted prefixes like "sql" in the output
        sql_query = sql_query.lstrip("sql").strip()
        print(f"line 107 sql querry generated {sql_query}")
        return sql_query
    except Exception as e:
        print(f"line 110 Error generating SQL query: {e}")
        return None

# Execute the SQL query
def execute_query(query):
    # query='SELECT * FROM Employees'
    try:
        try:
            cursor = conn_cursor().cursor()
            cursor.execute(query)
            df=cursor.fetchall()
            
        except Exception as e:
            print(f'line 123 exception occours as {e}')
            engine = create_connection()
            if engine is None:
                df = pd.DataFrame()
            else:
                df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print(f"line 131 Error executing SQL query: {e}")
        return None

# Handle user's natural language query
def handle_query(natural_language_query,model):
    # print(f"User Query: {natural_language_query}")
    sql_query = nl_to_sql(natural_language_query.get("statement"),model)
    if not sql_query:
        return "Failed to generate SQL query. Please try again."
    # print(f"line 140 Generated SQL Query: {sql_query}")
    result_df = execute_query(sql_query)
    if not result_df:
        return "No results found or query execution failed."
    return result_df

