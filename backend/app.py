from flask import Flask, request, jsonify, send_from_directory
import pickle
import os
from dotenv import load_dotenv
import logging

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

PORT = int(os.getenv('PORT', 5000))

# Load the trained model and product IDs
try:
    with open('cosine_sim.pkl', 'rb') as f:
        cosine_sim = pickle.load(f)
    with open('product_ids.pkl', 'rb') as f:
        product_ids = pickle.load(f)
except FileNotFoundError as e:
    logging.error(f"File not found: {e}")
    raise
except pickle.PickleError as e:
    logging.error(f"Error loading pickle file: {e}")
    raise

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Recommendation API"})

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        user_data = request.json
        purchased_product_ids = user_data.get('purchase_history', [])

        # Validate the format of purchase_history
        if not isinstance(purchased_product_ids, list) or not all(isinstance(pid, str) for pid in purchased_product_ids):
            return jsonify({"error": "Invalid input format. 'purchase_history' should be a list of strings."}), 400

        # Ensure there are IDs provided
        if not purchased_product_ids:
            return jsonify({"recommendations": []})

        # Find indices of the purchased products
        indices = [product_ids.index(pid) for pid in purchased_product_ids if pid in product_ids]

        if not indices:
            return jsonify({"recommendations": []})

        # Calculate average similarity scores
        sim_scores = [cosine_sim[idx] for idx in indices]
        avg_sim_scores = sum(sim_scores) / len(sim_scores)
        sim_scores = list(enumerate(avg_sim_scores))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Generate recommendations
        recommended_indices = [i[0] for i in sim_scores if i[0] not in indices][:5]
        recommended_products = [{'product_id': product_ids[i]} for i in recommended_indices]

        return jsonify({"recommendations": recommended_products})
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"error": "An internal error occurred. Please try again later."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
