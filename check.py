# Date format in YYYY/MM/DD

# Get email details
for email in emails:
    msg_id = email['id']
    message = get_message(service, msg_id)
    
    if message:
        print(f"Sender: {message['from']}")
        print(f"Body: {message['body'][:100]}...")  # Display first 100 chars
