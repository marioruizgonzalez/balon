from flask import Flask, render_template, jsonify
import psycopg2

app = Flask(__name__)

@app.route('/scatter-data')
def scatter_data():
    conn = psycopg2.connect(
        host="localhost",
        database="labasefemenil",
        user="marioruiz",
        password="welcome1"
    )
    cursor = conn.cursor()

    query = """
    SELECT 
        jugador AS player_name, 
        SUM(goles) AS goals, 
        SUM(mj) AS matches_played
    FROM 
        public.lbf_goleo_hist
    GROUP BY 
        jugador
    ORDER BY 
        goals DESC
    LIMIT 10;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    data = [{"player_name": row[0], "goals": row[1], "matches_played": row[2]} for row in rows]
    return jsonify(data)


# Database Connection: Fetch top 10 scorers
def get_top_scorers():
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host="localhost",
        database="labasefemenil",
        user="marioruiz",
        password="welcome1"
    )
    cursor = conn.cursor()

    # Query to fetch top 10 players with the most goals
    query = """
    SELECT 
        jugador AS player_name, 
        SUM(goles) AS total_goals
    FROM 
        public.lbf_goleo_hist
    GROUP BY 
        jugador
    ORDER BY 
        total_goals DESC
    LIMIT 10;
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    # Convert data into a list of dictionaries
    data = [{"player_name": row[0], "total_goals": row[1]} for row in rows]
    conn.close()
    return data

    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    # This was the original data function. You can rename or repurpose it.
    return jsonify([])

@app.route('/top-scorers')
def top_scorers():
    data = get_top_scorers()
    return jsonify(data)

@app.route('/estadistica-femenil')
def estadistica_femenil():
    return render_template('estadistica-femenil.html')

@app.route('/sheplays-analytics')
def sheplays_analytics():
    return render_template('sheplays-analytics.html')

if __name__ == '__main__':
    app.run(debug=True)
