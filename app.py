from flask import Flask, jsonify

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "name": "Keyboard", "price": 1299},
    {"id": 2, "name": "Mouse", "price": 599},
]


@app.get("/")
def home():
    return jsonify({"service": "shop-api", "message": "Shop API is running"})


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.get("/products")
def products():
    return jsonify(PRODUCTS), 200
