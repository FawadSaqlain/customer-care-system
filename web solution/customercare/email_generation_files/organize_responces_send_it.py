import smtplib
from email.message import EmailMessage



def generate_message_from_response(subject,body,response,model):
    prompt = f"Generate a response to the body: {body}. The raw response in parts is: {response}. Format the response in a clear, well-structured manner, ensuring it is polite, informative, and addresses all aspects of the inquiry. Do not add or remove any information; just make it well-structured and concise. Combine all parts into a single, cohesive message."    # Generate content using the model
    response = model.generate_content(prompt)
    return response.text


# -----------------------------------
# 3. SENDING EMAILS
# -----------------------------------
def send_email(to_email, subject, body):
    """
    Sends an email using SMTP. The email includes the recipient's address,
    subject, and body content.
    """
    msg = EmailMessage()
    msg['From'] = 'your_email@example.com'  # Replace with your email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('saqlainfawad@gmail.com', 'icft vsdq vbna kvhy')  # Replace with your credentials
        smtp.send_message(msg)
