import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from mysql.connector import pooling


app = Flask(__name__)

@app.route("/")
def home():
    return "Flask is running on Railway 🚀"

CORS(app)

# Database connection pool
import os

db_pool = pooling.MySQLConnectionPool(
    pool_name="portfolio_pool",
    pool_size=5,
    host=os.getenv("MYSQL_HOST"),
    port=int(os.getenv("MYSQL_PORT", 3306)),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)


# 🔹 Serve portfolio.html
@app.route("/")
def home():
    return render_template("portfolio.html")

# 🔹 Contact API
@app.route("/contact", methods=["POST"])
def contact():
    data = request.json

    conn = db_pool.get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO contact_messages (name, email, message) VALUES (%s, %s, %s)",
        (data["name"], data["email"], data["message"])
    )
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

