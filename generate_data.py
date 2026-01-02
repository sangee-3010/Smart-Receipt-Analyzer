import pandas as pd

# Creating a list of common receipt items and their categories
data = [
    # Merchant, Description, Category
    ["Starbucks", "Caramel Macchiato", "Food & Dining"],
    ["McDonalds", "Big Mac Meal", "Food & Dining"],
    ["Uber", "Ride to Airport", "Transport"],
    ["Shell", "Gasoline Petrol", "Transport"],
    ["Amazon", "Wireless Mouse", "Shopping"],
    ["Walmart", "Grocery Essentials", "Shopping"],
    ["Netflix", "Monthly Subscription", "Bills"],
    ["Airtel", "Phone Bill", "Bills"],
    ["CVS Pharmacy", "Painkillers", "Health"],
    ["City Hospital", "Consultation Fee", "Health"]
] * 10  # This multiplies the list so we have 100 rows total

# Turn it into a Table (DataFrame)
df = pd.DataFrame(data, columns=["merchant_name", "description", "category"])

# Add a random amount column for the "Insights" part later
import random
df['amount'] = [round(random.uniform(5.0, 100.0), 2) for _ in range(len(df))]

# Save it to your data folder
df.to_csv('data/dataset.csv', index=False)
print("Success! Created data/dataset.csv with 100 rows.")