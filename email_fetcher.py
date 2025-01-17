import os
import base64
import json
import re
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
import requests
from datetime import datetime

# If modifying, delete the token.json file to reauthorize
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Authenticate with Gmail API"""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8888)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)

def list_emails(service, label_ids=['INBOX'], start_date=None, end_date=None):
    """List emails in the inbox with date range filter"""
    try:
        # Build the search query based on the provided date range
        query = ''
        if start_date:
            query += f"after:{start_date} "
        if end_date:
            query += f"before:{end_date}"
        
        # Call Gmail API to list emails
        results = service.users().messages().list(userId='me', labelIds=label_ids, q=query).execute()
        messages = results.get('messages', [])
        
        if not messages:
            print('No new messages.')
            return []
        
        print('Messages:')
        return messages
    except HttpError as error:
        print(f'An error occurred: {error}')
        return []

def get_message(service, msg_id):
    """Get email content"""
    try:
        msg = service.users().messages().get(userId='me', id=msg_id).execute()
        payload = msg['payload']
        headers = payload['headers']
        parts = payload.get('parts', [])
        
        for header in headers:
            if header['name'] == 'From':
                sender = header['value']
        
        # Email body (may be in parts or plain text)
        body = ''
        if parts:
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
        else:
            body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        
        return {'from': sender, 'body': body}
    
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

# start_date = '2025/01/14'  # Start date
# end_date = '2025/01/15'    # End date

# # Authenticate and fetch emails within the date range
# service = authenticate_gmail()
# emails = list_emails(service, start_date=start_date, end_date=end_date)


# for email in emails:
#     msg_id = email['id']
#     message = get_message(service, msg_id)
    
#     if message:
#         email_body = message['body']
#         print(email_body)
