import imaplib
imap = imaplib.IMAP4_SSL('imap.gmail.com')
imap.login('saqlainfawad@gmail.com', 'icft vsdq vbna kvhy')  # Replace with your credentials
imap.select('inbox')
_, messages = imap.search(None, 'UNSEEN')  # Fetch unread emails