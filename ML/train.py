import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib

# 1. Load your actual CSV dataset
try:
    # Double check your folder name (you used 'DATA' in your snippet)
    df = pd.read_csv('/Users/sange/OneDrive/Documents/SRA/Smart-Receipt-Analyzer/DATA/dataset.csv')
    
    # Fill any empty descriptions to avoid errors
    df['merchant_name'] = df['merchant_name'].fillna('')
    df['description'] = df['description'].fillna('')
    
    X = df['merchant_name'] + " " + df['description']
    y = df['category']
    print(f"Loaded {len(df)} rows from dataset.csv")
except FileNotFoundError:
    print("Error: DATA/dataset.csv not found!")
    exit()

# 2. Build a more robust Pipeline
model_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english', ngram_range=(1, 2))),
    # Added class_weight='balanced' to help with imbalanced data
    ('clf', LogisticRegression(max_iter=1000, class_weight='balanced')) 
])

# 3. Train the model
print("Training the model on your dataset...")
model_pipeline.fit(X, y)

# 4. Save the "Brain"
joblib.dump(model_pipeline, 'expense_model.pkl')
print("Model saved as expense_model.pkl")

# 5. Quick Test
test_queries = ["Dunkin Donuts Coffee", "Uber to office", "Walmart groceries"]
print("-" * 30)
for query in test_queries:
    prediction = model_pipeline.predict([query])[0]
    print(f"Test Prediction for '{query}': {prediction}")
print("-" * 30)