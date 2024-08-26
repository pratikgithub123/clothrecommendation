import pickle
import json
import numpy as np

def convert_pickle_to_json(pickle_file, json_file):
    try:
        with open(pickle_file, 'rb') as f:
            data = pickle.load(f)
        
        # Convert numpy arrays to lists
        if isinstance(data, np.ndarray):
            data = data.tolist()
        
        with open(json_file, 'w') as f:
            json.dump(data, f)
        
        print(f"Successfully converted {pickle_file} to {json_file}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    convert_pickle_to_json('cosine_sim.pkl', 'cosine_sim.json')
    convert_pickle_to_json('product_ids.pkl', 'product_ids.json')
