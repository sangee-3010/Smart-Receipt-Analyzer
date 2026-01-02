import pandas as pd
import easyocr
import joblib
import os

# 1. Initialize OCR Reader (loads once to save time)
# 'en' for English; it downloads the model on the first run
reader = easyocr.Reader(['en'])

# 2. Helper for Prediction
def get_prediction(text):
    """Loads the model and predicts the category of the text."""
    try:
        # Assuming your model was saved in the 'ml' or 'models' folder
        model_path = 'expense_model.pkl' 
        if not os.path.exists(model_path):
            return "Uncategorized"
            
        model = joblib.load(model_path)
        prediction = model.predict([text])
        return prediction[0]
    except Exception as e:
        print(f"Prediction Error: {e}")
        return "Others"

# 3. OCR Function
def extract_text_from_image(image_path):
    """Extracts raw text from an image file."""
    try:
        # detail=0 returns a simple list of strings
        results = reader.readtext(image_path, detail=0)
        full_text = " ".join(results)
        return full_text
    except Exception as e:
        return f"Error: {str(e)}"

# 4. Your Spending Insights Logic
def generate_spending_insights(transactions_list):
    """Analyzes a list of transaction dictionaries for trends and patterns."""
    if not transactions_list or len(transactions_list) == 0:
        return {"message": "No data available."}

    df = pd.DataFrame(transactions_list)
    
    # Ensure amount is numeric
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)
    
    # Basic Aggregations
    total_spend = df['amount'].sum()
    category_totals = df.groupby('category')['amount'].sum().to_dict()

    # Find Top Category
    if category_totals:
        top_category = max(category_totals, key=category_totals.get)
        top_value = category_totals[top_category]
    else:
        top_category, top_value = "N/A", 0

    # Monthly Trend Logic
    try:
        df['date'] = pd.to_datetime(df['date'])
        # Get latest month in the data
        max_month = df['date'].dt.month.max()
        current_month_data = df[df['date'].dt.month == max_month]
        prev_month_data = df[df['date'].dt.month == (max_month - 1)]

        current_total = current_month_data['amount'].sum()
        prev_total = prev_month_data['amount'].sum()

        increase_pct = 0
        if prev_total > 0:
            increase_pct = ((current_total - prev_total) / prev_total) * 100
    except Exception:
        current_total, increase_pct = total_spend, 0

    return {
        "total_spending": round(total_spend, 2),
        "category_distribution": category_totals,
        "top_category": {
            "name": top_category,
            "amount": round(top_value, 2)
        },
        "monthly_summary": {
            "current_month_total": round(current_total, 2),
            "increase_percentage": round(increase_pct, 1)
        },
        "recommendation": f"Your highest spending is in {top_category}. Try to cut back there next week!"
    }

def get_prediction(text):
    text = text.lower()
    
    # Simple Keyword Overrides (The "Safety Net")
    if any(word in text for word in ['coffee', 'mcdonalds', 'food', 'restaurant', 'dinner', 'cafe']):
        return "Food & Dining"
    if any(word in text for word in ['uber', 'fuel', 'gas', 'petrol', 'train', 'metro']):
        return "Transport"
        
    # If no keywords found, use the ML model
    try:
        model = joblib.load('expense_model.pkl')
        return model.predict([text])[0]
    except:
        return "Others"