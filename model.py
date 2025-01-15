from email_fetcher import authenticate_gmail, list_emails, get_message
from phishing_checker import check_phishing

start_date = '2025/01/14'  # Start date
end_date = '2025/01/15'    # End date

# Authenticate and fetch emails within the date range
service = authenticate_gmail()
emails = list_emails(service, start_date=start_date, end_date=end_date)


for email in emails:
    msg_id = email['id']
    message = get_message(service, msg_id)
    
    if message:
        email_body = message['body']
        check_phishing(email_body)