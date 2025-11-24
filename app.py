from flask import Flask, render_template
import mysql.connector, secrets

app = Flask(__name__)

@app.route('/')
def home():
    # Connect to MySQL/MariaDB
    conn = mysql.connector.connect(
        host=secrets.host,
        user=secrets.user,
        password=secrets.password,
        database=secrets.database
    )
    cursor = conn.cursor()
    cursor.execute("SELECT 'Hello from MySQL!'")
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    greeting = result[0] if result else "Hello!"
    return render_template("home.html", greeting=greeting)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
