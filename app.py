import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("portfolio.html")

@app.route("/contact", methods=["POST"])
def contact():
    data = request.json
    print("Contact message received:", data)

    return jsonify({"status": "success"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
