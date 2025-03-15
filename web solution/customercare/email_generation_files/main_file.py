

# import imaplib
# import smtplib
# import email
# from email.message import EmailMessage
# from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
# import sqlite3
# import uuid
# import os
# from datetime import datetime
# import chardet  # Library to detect character encoding

import google.generativeai as genai
# import re
# import spacy
# import pandas as pd
# from sqlalchemy import create_engine
# import pyodbc
# importing header files
from. import fetch_mail as fm
from. import make_classification as mc
from. import complain_logs as cl
from. import answer_query as aq
from. import organize_responces_send_it as orsi

# Configure the Google Generative AI API
genai.configure(api_key="AIzaSyBA1FJ4OZsCDYla57Muc6EMS04ntEolrbE")
model = genai.GenerativeModel("gemini-1.5-flash")

# Load spaCy's model for Named Entity Recognition (NER)
# nlp_spacy = spacy.load("en_core_web_sm")

# -----------------------------------
# 6. GENERATING Appreciation RESPONSES
# -----------------------------------
def generate_response(body,subject):
    prompt = f"Generate a heartfelt and professional response to a message appreciating the subject '{subject}' and the body '{body}'. The message should convey gratitude, humility, and acknowledgment of the appreciation, while also reinforcing the positive relationship with the person expressing gratitude. The tone should be warm and respectful, expressing thanks for the recognition and openness for future collaboration or communication."
    # Generate content using the model
    response = model.generate_content(prompt)
    return response.text



# -----------------------------------
# 7. MAIN PROCESSING FUNCTION
# -----------------------------------
def process_emails():
    """
    Main function to process emails:
    1. Fetch unread emails.
    2. Classify each email as a complaint or query.
    3. Log complaints into the database and send acknowledgment.
    4. Generate responses for queries and send them back to the sender.
    """
    # setup_database()  # Ensure the database is ready
    emails = fm.fetch_emails()  # Fetch unread emails

    for email_data in emails:
        subject = email_data['subject']
        sender = email_data['from']
        body = email_data['body']

        #summerize the body
        summery= mc.summery_message(body,subject,model)
        print(f'summery :: {summery}')
        parts= mc.parse_categorized_response(summery)

        response=[]

        for part in parts:
            # Classify email
            classification = mc.classify_email(part)
            print(f"part :: {part}")
            print(f'classification :: {classification}')
            

            if classification == 'complaint':
                # Log complaint and send acknowledgment
                complaint_id = cl.log_complaint(sender, subject, body)
                response.append(f"Dear Customer,\n\nYour complaint has been logged with the ID: {complaint_id}.\nWe will address it as soon as possible.\n\nThank you.")
            elif classification == 'question':
                # Example usage
                if __name__ == "__main__":
                    user_query = part
                    result = aq.handle_query(user_query,model)
                    print(aq.handle_query({'statement':"Could you provide details on the product with the highest unit price?"}))
                    print(f"Query Result:\n{result}")
                    response.append(f"Dear Customer,\n\n{result}.\n\nThank you.")
            elif classification == 'appreciation':
                response.append(generate_response(body,subject))
            else:
                pass
            print(f"response :: {response}")
        if response:
            messaage=orsi.generate_message_from_response(subject,body,response,model)
            orsi.send_email(sender, f"Re: {subject}", messaage)

