import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load the CSV file into a DataFrame
file_path = r'C:backend/reccommend/products.csv'
df = pd.read_csv(file_path)

# Display basic info
print(df.info())

# Handle missing values
df['productDescription'].fillna('No description available', inplace=True)
df['productPrice'].fillna(df['productPrice'].mean(), inplace=True)

# Remove duplicates
df = df.drop_duplicates()

# Fix data types
df['productPrice'] = df['productPrice'].astype(float)
df['createdAt'] = pd.to_datetime(df['createdAt'])

# Handle outliers
df = df[df['productPrice'] <= 5000]

# Standardize and normalize data
df['productCategory'] = df['productCategory'].str.lower()
scaler = MinMaxScaler()
df[['productPrice']] = scaler.fit_transform(df[['productPrice']])

# Save cleaned data
df.to_csv('C:\Users\Acer\Desktop\Redommendation\clothrecommendation\backend\reccommend\cleaned_products.csv', index=False)
