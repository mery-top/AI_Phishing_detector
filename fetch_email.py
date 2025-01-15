import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Gmail API scope
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

def list_emails(service, label_ids=['INBOX']):
    """List emails in the inbox"""
    try:
        results = service.users().messages().list(userId='me', labelIds=label_ids).execute()
        messages = results.get('messages', [])
        if not messages:
            print('No new messages.')
            return []
        print('Messages:')
        for message in messages[:5]:  # Display first 5 messages for testing
            print(f"Message ID: {message['id']}")
        return messages
    except HttpError as error:
        print(f'An error occurred: {error}')
        return []

# Authenticate and fetch emails
service = authenticate_gmail()

# Test: List first 5 emails from the inbox
emails = list_emails(service)
