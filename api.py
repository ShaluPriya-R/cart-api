from flask import Flask, request, jsonify
import json

app = Flask(__name__)
CART_FILE = 'carts.json'

def load_carts():
    with open(CART_FILE, 'r') as f:
        return json.load(f)

def save_carts(data):
    with open(CART_FILE, 'w') as f:
        json.dump(data, f, indent=2)

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
        if cart['id'] == cart_id:
            return jsonify(cart)
    return jsonify({'error': 'Cart not found'}), 404

@app.route('/add_cart', methods=['POST'])
def add_cart():
    new_cart = request.json
    data = load_carts()
    data['carts'].append(new_cart)
    save_carts(data)
    return jsonify({'message': 'Cart added successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
