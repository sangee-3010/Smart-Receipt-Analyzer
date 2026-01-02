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

    # Save the file
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # 1. OCR: Get text from image (Uses the OpenCV + EasyOCR logic)
    extracted_text = extract_text_from_image(filepath)

    # 2. ML: Predict category
    category = get_prediction(extracted_text)

    # CLEANUP FOR FRONTEND: 
    # We send the full text for the database, but a snippet for the demo UI
    return jsonify({
        "status": "success",
        "category": category,
        "extracted_text_full": extracted_text,
        "display_text": extracted_text[:150] + "..." if len(extracted_text) > 150 else extracted_text,
        "file_path": filepath
    })

@app.route('/predict-text', methods=['POST'])
def predict_text():
    """Endpoint for manual text entry or digital receipts."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
        
    text = data.get('text', '')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
        
    category = get_prediction(text)
    return jsonify({
        "status": "success",
        "text": text,
        "category": category
    })

@app.route('/get-insights', methods=['POST'])
def get_insights():
    """Endpoint for generating dashboard analytics."""
    # Expecting a list of transaction objects from Member B
    transactions = request.get_json() 
    if not transactions:
        return jsonify({"error": "No transaction data provided"}), 400
        
    insights = generate_spending_insights(transactions)
    return jsonify(insights)

if __name__ == '__main__':
    # host='0.0.0.0' allows Member B to connect from their computer on the same Wi-Fi
    app.run(host='0.0.0.0', port=5000, debug=True)