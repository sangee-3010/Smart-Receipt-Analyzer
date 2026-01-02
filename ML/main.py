import os
from flask import Flask, request, jsonify
from utils import extract_text_from_image, get_prediction, generate_spending_insights

app = Flask(__name__)

# Create a folder to save uploaded receipts
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload-receipt', methods=['POST'])
def upload_receipt():
    """Endpoint for uploading a physical receipt image."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save the file temporarily
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # 1. OCR: Get text from image
    extracted_text = extract_text_from_image(filepath)

    # 2. ML: Predict category from that text
    category = get_prediction(extracted_text)

    return jsonify({
        "status": "success",
        "extracted_text": extracted_text,
        "category": category,
        "file_path": filepath
    })

@app.route('/predict-text', methods=['POST'])
def predict_text():
    """Endpoint for manual text entry or digital receipts."""
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
        
    category = get_prediction(text)
    return jsonify({
        "text": text,
        "category": category
    })

@app.route('/get-insights', methods=['POST'])
def get_insights():
    """Endpoint for generating dashboard analytics."""
    # Member B sends the list of transactions from their database
    transactions = request.get_json() 
    insights = generate_spending_insights(transactions)
    return jsonify(insights)

if __name__ == '__main__':
    # Running on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)