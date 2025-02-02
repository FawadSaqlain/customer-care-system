import google.generativeai as genai

genai.configure(api_key="AIzaSyBA1FJ4OZsCDYla57Muc6EMS04ntEolrbE")
# model = genai.GenerativeModel("gemini-1.5-flash")
# response = model.generate_content("give me sql querry to get all the data from employ table")
# print(response.text)



import re
import spacy
import pandas as pd
# from transformers import pipeline
from sqlalchemy import create_engine
import pyodbc
# Load spaCy's model for Named Entity Recognition (NER)
nlp_spacy = spacy.load("en_core_web_sm")

# Load the NLP model for text-to-SQL conversion
# nlp_model = pipeline("text2text-generation", model="mrm8488/t5-base-finetuned-wikiSQL")
model = genai.GenerativeModel("gemini-1.5-flash")

# Create a database connection using SQLAlchemy
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
    
    conn = pyodbc.connect(conn_str)
    if conn:
        print("Connected to MSSQL Server successfully using Windows Authentication!")
        return conn
    else:
        return None


# # Connect to the database



# cursor = conn.cursor()

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

def preprocess_query(natural_language_query):
    # Use NER to extract entities from the query
    doc = nlp_spacy(natural_language_query)
    for ent in doc.ents:
        if ent.label_ == "GPE":  # Geopolitical entity (city, country)
            natural_language_query = natural_language_query.replace(ent.text, f"'{ent.text}'")

    # Replace common terms with schema-specific terms
    for table, columns in TABLE_COLUMN_MAPPING.items():
        # Replace table names
        natural_language_query = re.sub(rf"\b{table}\b", table, natural_language_query, flags=re.IGNORECASE)
        # Replace column names
        for column in columns:
            natural_language_query = re.sub(rf"\b{column}\b", column, natural_language_query, flags=re.IGNORECASE)

    # Remove unnecessary words for cleaner SQL generation
    stopwords = ["list of", "show me", "all the", "who"]
    for word in stopwords:
        natural_language_query = natural_language_query.replace(word, "")

    # Ensure the query is framed to be more SQL-like
    return natural_language_query.strip()

# Modify the SQL generation to match the table and column structure
def nl_to_sql(natural_language_query):
    try:
        # Preprocess the natural language query
        cleaned_query = preprocess_query(natural_language_query)
        print(f'** print the cleaned query :: {cleaned_query}')
        # Generate SQL query using NLP model
        prompt = f"Translate the following natural language question into an SQL query . Ensure the query retrieves the necessary data from the appropriate table(s) and includes proper syntax: {cleaned_query} according to this database schema : {TABLE_COLUMN_MAPPING}"
        # sql_query = nlp_model(prompt)[0]['generated_text'].strip()
        sql_query = model.generate_content(prompt)
        print(f'query generated :: {sql_query.text}')

        # # Ensure the query starts with SELECT and contains a valid table
        # if not sql_query.text.lower().startswith("select"):
        #     print('Default fallback for missing SELECT')
        #     sql_query = "SELECT name FROM sys.tables"
        # #     sql_query = f"SELECT * FROM Employees"  # Default fallback for missing SELECT

        # # Fix the query structure if the table name is missing or incorrect
        # if "FROM" not in sql_query:
        #     print('# Default fallback table')
        #     sql_query = "SELECT name FROM sys.tables"

        # #     sql_query = f"SELECT * FROM Employees"  # Default fallback table

        return sql_query.text
    except Exception as e:
        print(f"Error generating SQL query: {e}")
        return None

# Validate and correct SQL queries
def validate_and_correct_sql(sql_query):
    try:
        # Check for required SQL components
        if not all(keyword in sql_query.upper() for keyword in ["SELECT", "FROM"]):
            print("SQL query is incomplete.")
            return None

        # Format string literals
        sql_query = re.sub(r"\b([A-Za-z]+)\b", r"'\1'", sql_query)

        # Basic syntax correction for WHERE clauses
        if "WHERE" in sql_query.upper() and "=" not in sql_query:
            sql_query = re.sub(r"WHERE (.+)", r"WHERE \1 = 'value'", sql_query, flags=re.IGNORECASE)

        return sql_query
    except Exception as e:
        print(f"Error validating/correcting SQL query: {e}")
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
            print(f'exception occours as {e}')
            engine = create_connection()
            if engine is None:
                df = pd.DataFrame()
            else:
                df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print(f"Error executing SQL query: {e}")
        return pd.DataFrame()

# Handle user's natural language query
def handle_query(natural_language_query):
    print(f"Received natural language query: {natural_language_query}")

    # Generate SQL from natural language
    sql_query = nl_to_sql(natural_language_query)
    
    if not sql_query:
        return "Failed to generate SQL query. Please try again."

    print(f"Generated SQL Query: {sql_query}")

    # Validate and correct the SQL query
    valid_sql_query = validate_and_correct_sql(sql_query)
    if not valid_sql_query:
        return "The generated SQL query is invalid. Please try rephrasing your query."

    print(f"Validated SQL Query: {valid_sql_query}")

    # Execute the SQL query and fetch results
    result_df = execute_query(valid_sql_query)
    print(f'result_df :: {result_df}')
    if not result_df:
        return "No results found or query execution failed."

    return result_df

# Example usage
if __name__ == "__main__":
    user_query = "Show me the list of all the Shippers"
    result = handle_query(user_query)
    print(f"Query Result:\n{result}")
