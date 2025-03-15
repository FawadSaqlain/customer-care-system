import imaplib
import email
import chardet

# -----------------------------------
# 2. FETCHING UNREAD EMAILS
# -----------------------------------


def fetch_emails():
    """
    Connects to the Gmail IMAP server, fetches unread emails from the inbox,
    and extracts their content (subject, sender, and body).
    """
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login('saqlainfawad@gmail.com', 'icft vsdq vbna kvhy')  # Replace with your credentials
    imap.select('inbox')
    _, messages = imap.search(None, 'UNSEEN')  # Fetch unread emails
    # print(f' line 14 messages :: {messages}')
    # print(f' line 15 messages :: {_}')

    email_ids = messages[0].split()
    # print(f' line 18 email_ids :: {email_ids}')
    emails = []
    for eid in email_ids:
        _, msg_data = imap.fetch(eid, '(RFC822)')
        # print(f' line 22 msg_data :: {msg_data}')
        # print(f' line 23 msg_data :: {_}')
        raw_email = msg_data[0][1]
        # print(f' line 25 raw_email :: {raw_email}')
        msg = email.message_from_bytes(raw_email)
        # print(f' line 27 msg :: {msg}')

        # Extract the body of the email
        body = None
        if msg.is_multipart():  # For emails with multiple parts
            for part in msg.walk():
                content_type = part.get_content_type()
                # print(f' line 34 content_type :: {content_type}')
                content_disposition = str(part.get("Content-Disposition"))
                # print(f' line 36 content_disposition :: {content_disposition}')

                if content_type == "text/plain" and "attachment" not in content_disposition:
                    raw_body = part.get_payload(decode=True)
                    # print(f' line 40 raw_body :: {raw_body}')
                    if raw_body:
                        encoding = chardet.detect(raw_body)['encoding'] or 'utf-8'
                        body = raw_body.decode(encoding, errors='replace')
                        # print(f' line 44 body :: {body}')
                        break
        else:  # For single-part emails
            raw_body = msg.get_payload(decode=True)
            if raw_body:
                encoding = chardet.detect(raw_body)['encoding'] or 'utf-8'
                # print(f' line 50 encoding :: {encoding}')
                body = raw_body.decode(encoding, errors='replace')
                # print(f' line 52 body :: {body}')

        emails.append({
            'subject': msg['subject'] or "No Subject",
            'from': msg['from'] or "Unknown Sender",
            'body': body or "No Content"
        })
        # print(f' line 59 emails :: {emails}')
    imap.close()
    imap.logout()
    return emails
