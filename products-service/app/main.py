from flask import Flask, jsonify, request

app = Flask(__name__)

# Temporary in-memory product list (later we can replace this with a real database)
PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 1200.0},
    {"id": 2, "name": "Mouse", "price": 25.0},
]


@app.route("/health", methods=["GET"])
def health():
    """
    Health-check endpoint.
    Used by monitoring systems, load balancers, and CI/CD pipelines
    to confirm that the service is running properly.
    """
    return jsonify({"status": "ok", "service": "products"}), 200


@app.route("/products", methods=["GET"])
def list_products():
    """
    Return the full list of products.
    This is a simple GET endpoint for reading data.
    """
    return jsonify(PRODUCTS), 200


@app.route("/products", methods=["POST"])
def create_product():
    """
    Create a new product.
    Expects JSON body containing: "name" and "price".
    """
    data = request.get_json()

    # Validate request body (must contain 'name' and 'price')
    if data is None or "name" not in data or "price" not in data:
        return jsonify({"error": "name and price are required"}), 400

    # Generate a new ID (auto-increment)
    new_id = max((p["id"] for p in PRODUCTS), default=0) + 1

    # Build the new product dictionary
    product = {
        "id": new_id,
        "name": data["name"],
        "price": float(data["price"]),
    }

    # Add the new product to the list
    PRODUCTS.append(product)

    # Return created product with status code 201 (Created)
    return jsonify(product), 201


if __name__ == "__main__":
    # Local development server. In production we run this using Docker + WSGI.
    app.run(host="0.0.0.0", port=5000)
    #Done
