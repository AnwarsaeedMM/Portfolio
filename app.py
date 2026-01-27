from flask import Flask, render_template, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# -------------------------------
# MySQL connection (Render-safe)
# -------------------------------
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),        # cloud3.googiehost.com
        user=os.environ.get("DB_USER"),        # ovrmxygd_portfolio_user
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        port=int(os.environ.get("DB_PORT", 3306))
    )

# -------------------------------
# Home Page
# -------------------------------
@app.route("/")
def home():
    return render_template("portfolio.html")  # your HTML file

# -------------------------------
# Contact Form API
# -------------------------------
@app.route("/contact", methods=["POST"])
def contact():
    try:
        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        if not name or not email or not message:
            return jsonify({"status": "error", "msg": "All fields required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO contact_messages (name, email, message)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (name, email, message))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"status": "success", "msg": "Message saved successfully!"})

    except Exception as e:
        print("DB ERROR:", e)
        return jsonify({"status": "error", "msg": str(e)}), 500

# -------------------------------
# DB Test Route (REMOVE AFTER TEST)
# -------------------------------
@app.route("/test-db")
def test_db():
    try:
        conn = get_db_connection()
        conn.close()
        return "✅ Database connected successfully!"
    except Exception as e:
        return f"❌ Database error: {e}"

# -------------------------------
# Run App
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
