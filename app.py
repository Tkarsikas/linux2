from flask import Flask
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
 cursor.execute("SELECT NOW();")
 result = cursor.fetchone()
 # Clean up
 cursor.close()
 conn.close()
 return str(result[0])

@app.route('/time')
def api_time():
    return jsonify({"time": get_time()})

@app.route('/')
def home():
    return '''
    <html>
    <head>
        <title>MySQL Clock</title>
        <script>
            async function updateClock() {
                const response = await fetch('/time');
                const data = await response.json();
                document.getElementById('clock').innerText = data.time;
            }

            // Päivitä kello heti ja sen jälkeen joka sekunti
            setInterval(updateClock, 1000);
            window.onload = updateClock;
        </script>
    </head>
    <body style="font-family: Arial; text-align: center; margin-top: 100px; background-color: pink;">
        <h1>MySQL Server Time</h1>

        <!-- Kello -->
        <h2 id="clock" style="margin-bottom: 10px;">Loading...</h2>

        <!-- Nappi kellon ja giffin väliin -->
        <div style="text-align:center; margin-bottom: 10px;">
            <a href="http://86.50.23.190:8501/data-analysis/" 
                style="display: inline-block; padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px;">
                View Data Analysis
            </a>
        </div>

        <!-- Gif -->
        <div style="text-align:center;">
            <img src="/static/ursos-fritando-bear.gif" alt="animated gif" style="width: 600px;" />
        </div>

    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)