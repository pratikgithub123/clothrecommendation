import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load the extracted data
products = pd.read_csv('products.csv')

# Combine relevant fields into a single text column
products['text'] = products['tags'].apply(lambda x: ' '.join(eval(x))) + ' ' + products['productDescription']

# Convert the text data to a matrix of token counts (TF-IDF)
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(products['text'])
print(tfidf_matrix.shape) 

# Calculate cosine similarity between products
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
print(cosine_sim.shape)

# Save the model and product IDs
product_ids = products['_id'].tolist()

with open('cosine_sim.pkl', 'wb') as f:
    pickle.dump(cosine_sim, f)

with open('product_ids.pkl', 'wb') as f:
    pickle.dump(product_ids, f)

print("Model training completed and saved as 'cosine_sim.pkl' and 'product_ids.pkl'")
