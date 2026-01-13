from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION ---
DB_HOST = "localhost"
DB_NAME = "rasa_db"
DB_USER = "rasa_user"
DB_PASS = "rootadmin"
DB_PORT = "5432"

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    # 1. Handle GET requests (Browser visits)
    if request.method == 'GET':
        return "<h1>Server is running!</h1> <p>Go back to loginnew.html and click the Login button to test.</p>"

    # 2. Handle POST requests (Actual Login)
    username = request.form.get('txtLoginName')
    password = request.form.get('txtPassword')

    if not username or not password:
        return jsonify({"status": "error", "message": "Missing username or password"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"status": "error", "message": "Database error"}), 500

    try:
        cursor = conn.cursor()
        query = "SELECT * FROM wbauthusers WHERE loginname = %s AND hashpwd = %s;"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return jsonify({
                "status": "success", 
                "message": "Login Successful", 
                "user_name": user[3],
                "roll_number": user[1]
            })
        else:
            return jsonify({"status": "error", "message": "Invalid Username or Password"}), 401

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": "Server error"}), 500

if __name__ == '__main__':
    print("🚀 Login Server is running on http://localhost:3000")
    app.run(port=3000, debug=True)