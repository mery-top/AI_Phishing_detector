import requests

def check_phishing(email_body):
    url = 'http://localhost:5555/predict'  # Your Flask app endpoint
    response = requests.post(url, json={'message': email_body})
    if response.status_code == 200:
        prediction = response.json().get('prediction')
        if prediction == 1:
            print("Phishing detected!")
        else:
            print("Email is safe.")
    else:
        print(f"Error: {response.text}")
