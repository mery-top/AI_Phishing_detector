# Date format in YYYY/MM/DD

import requests

# URL to test
test_url = {
    "url": "br-icloud.com.br"
}

# Make a POST request to the Flask API
response = requests.post("http://127.0.0.1:5555/detect", json=test_url)
print(response.json())
  # Display first 100 chars
