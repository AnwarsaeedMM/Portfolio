import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from mysql.connector import pooling

app = Flask(__name__)
CORS(app)

# -------------------------
# SAFE DB POOL (lazy load)
# -------------------------
db_pool = None

def get_db_pool():
    global db_pool
    if db_pool is None:
        db_pool = pooling.MySQLConnectionPool(
            pool_name="portfolio_pool",
            pool_size=5,
            host=os.environ["MYSQL_HOST"],
            port=int(os.environ.get("MYSQL_PORT", 3306)),
            user=os.environ["MYSQL_USER"],
            password=os.environ["MYSQL_PASSWORD"],
            database=os.environ["MYSQL_DATABASE"]
        )
    return db_pool

# -------------------------
# Routes
# -------------------------
@app.route("/")
def home():
    return render_template("portfolio.html")

@app.route("/health")
def health():
    return "OK"

@app.route("/contact", methods=["POST"])
def contact():
    data = request.json

    pool = get_db_pool()
    conn = pool.get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO contact_messages (name, email, message) VALUES (%s, %s, %s)",
        (data["name"], data["email"], data["message"])
    )
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"status": "success"})

# -------------------------
# Local run only
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
