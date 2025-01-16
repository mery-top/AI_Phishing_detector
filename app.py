from flask import Flask, request, jsonify
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import tensorflow as tf
import numpy as np
import pickle


app = Flask(__name__)

model = BertForSequenceClassification.from_pretrained('phishing-detector')
tokenizer = BertTokenizer.from_pretrained('phishing-detector')


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

model2 = tf.keras.models.load_model('phishing_url_model.h5')
with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

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

@app.route('/detect', methods=['POST'])
def detect_phishing():
    if not model2 or not vectorizer:
        return jsonify({"error": "Model or vectorizer not loaded properly"}), 500

    try:
        # Parse incoming JSON request
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({"error": "Invalid input. Please provide a 'url' field."}), 400
        
        url = data['url']
        print(f"Received URL: {url}")

        # Define class labels before referencing them
        class_labels = ['benign', 'defacement', 'phishing', 'malware']
        
        # Transform the URL using the vectorizer
        url_features = vectorizer.transform([url]).toarray()
        print(f"Transformed features: {url_features.shape}")
        
        # Make a prediction
        prediction = model2.predict(url_features)
        print(f"Raw prediction output: {prediction}") 
        if prediction.ndim != 2 or prediction.shape[1] != len(class_labels):
            raise ValueError(f"Unexpected prediction shape: {prediction.shape}")
        
        class_idx = np.argmax(prediction)
        class_label = class_labels[class_idx]
        confidence = prediction[0][class_idx]
        
        # Return the result
        return jsonify({
            'url': url,
            'type': class_label,
            'confidence': float(confidence)
        })
    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": f"An error occurred during detection: {str(e)}"}), 500

    



if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5555, debug = True)