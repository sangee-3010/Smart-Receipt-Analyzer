import pandas as pd
import easyocr
import joblib
import os
import cv2
import numpy as np

# 1. Initialize OCR Reader (Loaded once)
# Set gpu=False if you don't have an NVIDIA GPU; it prevents crashes.
reader = easyocr.Reader(['en'], gpu=False)

# 2. Hybrid Prediction Logic
def get_prediction(text):
    """Predicts category using a Hybrid Approach: Keywords + ML Model."""
    text_clean = text.lower().strip()
    
    # --- LEVEL 1: THE SAFETY NET (Keyword Overrides) ---
    safety_map = {
        "Food & Dining": ['starbucks', 'mcdonald', 'dunkin', 'donut', 'coffee', 'pizza', 'burger', 'restaurant', 'cafe', 'swiggy', 'zomato', 'kfc', 'subway'],
        "Transport": ['uber', 'lyft', 'shell', 'fuel', 'gas', 'petrol', 'train', 'metro', 'chevron', 'ola', 'rapido', 'exxon'],
        "Shopping": ['amazon', 'walmart', 'target', 'zara', 'nike', 'hm', 'flipkart', 'mall', 'best buy', 'ikea'],
        "Bills": ['netflix', 'airtel', 'verizon', 'utility', 'electricity', 'water', 'internet', 'subscription', 'comcast'],
        "Health": ['pharmacy', 'hospital', 'cvs', 'walgreens', 'doctor', 'clinic', 'medical', 'dentist']
    }

    for category, keywords in safety_map.items():
        if any(key in text_clean for key in keywords):
            return category

    # --- LEVEL 2: MACHINE LEARNING FALLBACK ---
    try:
        model_path = 'expense_model.pkl'
        if not os.path.exists(model_path):
            return "Others"
            
        model = joblib.load(model_path)
        prediction = model.predict([text_clean])
        return prediction[0]
    except Exception as e:
        print(f"Prediction Error: {e}")
        return "Others"

# 3. Image Preprocessing & OCR Function
def extract_text_from_image(image_path):
    """Cleans image with OpenCV and extracts text via OCR."""
    try:
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            return "Error: Could not read image file."

        # OpenCV Preprocessing: Grayscale -> Denoise -> Threshold
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        denoised = cv2.fastNlMeansDenoising(gray, h=10)
        _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Run OCR on the processed (black & white) image
        results = reader.readtext(thresh, detail=0)
        full_text = " ".join(results)
        
        return full_text
    except Exception as e:
        return f"Error during OCR: {str(e)}"

# 4. Spending Insights Logic
def generate_spending_insights(transactions_list):
    """Analyzes transaction data for trends and dashboard metrics."""
    if not transactions_list or len(transactions_list) == 0:
        return {"message": "No data available."}

    df = pd.DataFrame(transactions_list)
    
    # Data Cleaning
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)
    
    # Aggregations
    total_spend = df['amount'].sum()
    category_totals = df.groupby('category')['amount'].sum().to_dict()

    # Find Top Category
    if not df.empty and 'category' in df.columns:
        top_category = df.groupby('category')['amount'].sum().idxmax()
        top_value = category_totals[top_category]
    else:
        top_category, top_value = "N/A", 0

    # Monthly Comparison
    try:
        df['date'] = pd.to_datetime(df['date'])
        max_month = df['date'].dt.month.max()
        
        current_month_total = df[df['date'].dt.month == max_month]['amount'].sum()
        prev_month_total = df[df['date'].dt.month == (max_month - 1)]['amount'].sum()

        increase_pct = 0
        if prev_month_total > 0:
            increase_pct = ((current_month_total - prev_month_total) / prev_month_total) * 100
    except:
        current_month_total, increase_pct = total_spend, 0

    return {
        "total_spending": round(total_spend, 2),
        "category_distribution": category_totals,
        "top_category": {
            "name": top_category,
            "amount": round(top_value, 2)
        },
        "monthly_summary": {
            "current_month_total": round(current_month_total, 2),
            "increase_percentage": round(increase_pct, 1)
        },
        "recommendation": f"Your highest spending is in {top_category}. Consider reviewing these items."
    }