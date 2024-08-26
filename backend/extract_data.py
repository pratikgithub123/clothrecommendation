from pymongo import MongoClient
import pandas as pd

# Connect to MongoDB
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['recommendation']  # Replace with your actual database name

# Extract data from the products and orders collections
products = pd.DataFrame(list(db.products.find()))
users = pd.DataFrame(list(db.users.find()))
orders = pd.DataFrame(list(db.orders.find()))

# Example: Display the first few rows of the products collection
print(products.head())
print(users.head())
print(orders.head())

# Save the extracted data to CSV files (optional)
products.to_csv('products.csv', index=False)
users.to_csv('users.csv', index=False)
orders.to_csv('orders.csv', index=False)
