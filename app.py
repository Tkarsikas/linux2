from flask import Flask
import mysql.connector secrets
app = Flask(__name__)
@app.route('/')
def home():
    # Connect to MySQL/MariaDB
    conn = mysql.connector.connect(
    host=config.host,
    user=config.user,
    password=config.password,
    database=config.database
    )
    cursor = conn.cursor()
    cursor.execute("SELECT 'Hello from MySQL!'")
    result = cursor.fetchone()
    # Clean up
    cursor.close()
    conn.close()
    return f"<h1>{result[0]}</h1>"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)