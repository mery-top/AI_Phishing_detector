from flask import Flask, request, jsonify
from transformers import BertTokenizer, BertForSequenceClassification
import torch

app = Flask(__name__)

model = BertForSequenceClassification.from_pretrained('phishing-detector')
tokenizer = BertTokenizer.from_pretrained('phishing-detector')


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

def predict(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512).to(device)

    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()
        
    return predicted_class

@app.route('/')
def index():
    return "Hello World"



@app.route('/predict', methods=['POST'])
def predict_route():
    try:
        data = request.get_json()
        message = data['message']
        
        if not message:
            raise ValueError("Message is required")
        
        prediction = predict(message)
        
        return jsonify({'prediction': prediction})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5555, debug = True)