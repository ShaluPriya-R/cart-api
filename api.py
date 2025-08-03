from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
CART_FILE = 'carts.json'

# ----------- Helpers for NDJSON -----------

def load_carts():
    """Load carts from NDJSON file. One JSON object per line."""
    carts = []
    if os.path.exists(CART_FILE):
        with open(CART_FILE, 'r') as f:
            for line in f:
                if line.strip():  # Skip empty lines
                    try:
                        carts.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass  # Ignore invalid lines
    return {"carts": carts}

def save_carts(data):
    """Save carts to NDJSON file."""
    with open(CART_FILE, 'w') as f:
        for cart in data['carts']:
            json.dump(cart, f)
            f.write("\n")

# ----------- Routes -----------

@app.route('/')
def home():
    return "🛒 Cart API is running!"

@app.route('/carts', methods=['GET'])
def get_carts():
    data = load_carts()
    return jsonify(data)

@app.route('/cart/<int:cart_id>', methods=['GET'])
def get_cart(cart_id):
    data = load_carts()
    for cart in data['carts']:
        if cart.get('id') == cart_id:
            return jsonify(cart)
    return jsonify({'error': 'Cart not found'}), 404

@app.route('/add_cart', methods=['POST'])
def add_cart():
    new_cart = request.json
    data = load_carts()
    data['carts'].append(new_cart)
    save_carts(data)
    return jsonify({'message': 'Cart added successfully'}), 201

# ----------- Main -----------

if __name__ == '__main__':
    app.run(debug=True)
