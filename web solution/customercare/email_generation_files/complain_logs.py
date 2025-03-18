import uuid
# import sqlite3
from django.db import connection


# -----------------------------------
# 1. SETTING UP DATABASE
# -----------------------------------
# def setup_database():
#     """
#     Creates a SQLite database to store complaints. The table `complaints` will
#     store complaint ID, customer email, subject, body, and timestamp.
#     """
#     conn = sqlite3.connect('customer_care.db')  # Creates or connects to the database
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS complaints (
#             id TEXT PRIMARY KEY,  -- Unique ID for the complaint
#             email TEXT,           -- Customer email address
#             subject TEXT,         -- Subject of the email
#             body TEXT,            -- Body/content of the email
#             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP -- Timestamp of the complaint
#         )
#     ''')
#     conn.commit()
#     conn.close()


# -----------------------------------
# 5. LOGGING COMPLAINTS in the database customer_care.db
# -----------------------------------
def log_complaint(email, subject, body):
    """
    Logs complaints into the database with a unique ID.
    """
    # conn = sqlite3.connect('customer_care.db')
    # cursor = conn.cursor()
    with connection.cursor() as cursor:
        complaint_id = str(uuid.uuid4())  # Generate a unique ID for the complaint
        cursor.execute('''
        INSERT INTO complaints (id, email, subject, body)
        VALUES (%s, %s, %s, %s)
        ''', (complaint_id, email, subject, body))

        cursor.commit()
        cursor.close()
    return complaint_id

