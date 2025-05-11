import email
from imapclient import IMAPClient
from email.header import decode_header
from email.utils import parsedate_to_datetime
from app.config import EMAIL_ADDRESS, EMAIL_PASS, IMAP_SERVER, IMAP_PORT

def fetch_unseen_emails():
    with IMAPClient('imap.gmail.com') as client:
        client.login(EMAIL_ADDRESS, EMAIL_PASS)
        client.select_folder('INBOX')

        # Search for unseen (unread) emails
        messages = client.search(['UNSEEN'])
        print(f"Found {len(messages)} unread emails.")

        # Fetch the email bodies
        response = client.fetch(messages, ['RFC822'])

        emails = []

        for msgid, data in response.items():
            msg = email.message_from_bytes(data[b'RFC822'])

            subject = msg['subject']
            print(f"Subject: {subject}")

            # Decode the subject (sometimes the subject is encoded)
            decoded_subject, encoding = decode_header(subject)[0]
            if isinstance(decoded_subject, bytes):
                subject = decoded_subject.decode(encoding or 'utf-8')
            print(f"Decoded Subject: {subject}")

            # Handling multipart emails
            body = None
            if msg.is_multipart():
                for part in msg.walk():
                    # We only care about the text/plain part
                    if part.get_content_type() == 'text/plain':
                        try:
                            # Attempt to decode with UTF-8 first
                            body = part.get_payload(decode=True).decode('utf-8')
                        except UnicodeDecodeError:
                            # If UTF-8 fails, try ISO-8859-1 (latin1)
                            try:
                                body = part.get_payload(decode=True).decode('ISO-8859-1')
                            except Exception as e:
                                print(f"Error decoding email body: {e}")
                        break
            else:
                # If it's not multipart, directly decode
                try:
                    body = msg.get_payload(decode=True).decode('utf-8')
                except UnicodeDecodeError:
                    try:
                        body = msg.get_payload(decode=True).decode('ISO-8859-1')
                    except Exception as e:
                        print(f"Error decoding email body: {e}")

            # Store the email details
            emails.append({
                "subject": subject,
                "body": body
            })

        return emails
