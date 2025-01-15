from flask import Flask, render_template, jsonify
import psycopg2

app = Flask(__name__)

# Database Connection Configuration
DB_CONFIG = {
    "host": "localhost",
    "database": "labasefemenil",
    "user": "marioruiz",
    "password": "welcome1"
}

def get_db_connection():
    """Creates a database connection."""
    return psycopg2.connect(**DB_CONFIG)

# Existing Functionality
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/estadistica-femenil')
def estadistica_femenil():
    return render_template('estadistica-femenil.html')

@app.route('/sheplays-analytics')
def sheplays_analytics():
    return render_template('sheplays-analytics.html')

# 1. Top Scorers by Season
@app.route('/top-scorers')
def top_scorers():
    """Fetches top scorers."""
    conn = get_db_connection()
    cursor = conn.cursor()

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
    conn.close()

    data = [{"player_name": row[0], "total_goals": row[1]} for row in rows]
    return jsonify(data)

# 2. Efficiency of Scoring
@app.route('/api/efficiency')
def efficiency():
    """Fetches data for 'Efficiency of Scoring'."""
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        jugador AS player_name,
        SUM(mj) AS total_minutes_played,
        SUM(goles) AS total_goals,
        ROUND(SUM(goles)::NUMERIC / NULLIF(SUM(mj), 0), 2) AS goals_per_minute
    FROM 
        lbf_goleo
    GROUP BY 
        jugador
    ORDER BY 
        goals_per_minute DESC
    LIMIT 10;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    data = [{"player_name": row[0], "total_minutes_played": row[1], "total_goals": row[2], "goals_per_minute": row[3]} for row in rows]
    return jsonify(data)

# 3. Clubs with Fewer Youth Participation
@app.route('/api/youth-participation')
def youth_participation():
    """Fetches data for 'Youth Participation by Club'."""
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        club,
        SUM(minutos_acumulados_2) AS total_minutes_youth
    FROM 
        lbf_participacion_menores
    GROUP BY 
        club
    ORDER BY 
        total_minutes_youth ASC
    LIMIT 10;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    data = [{"club": row[0], "total_minutes_youth": row[1]} for row in rows]
    return jsonify(data)

# 4. Clubs with Most Cards per Minute
@app.route('/api/cards-per-minute')
def cards_per_minute():
    """Fetches data for 'Clubs with Most Cards per Minute Played'."""
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        club,
        SUM(total_tarjetas) AS total_cards,
        SUM(promedio_x_minutos) AS total_minutes,
        ROUND(SUM(total_tarjetas) / NULLIF(SUM(promedio_x_minutos), 0), 2) AS cards_per_minute
    FROM 
        lbf_tarjetas_club
    GROUP BY 
        club
    ORDER BY 
        cards_per_minute DESC
    LIMIT 10;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    data = [{"club": row[0], "cards_per_minute": row[3]} for row in rows]
    return jsonify(data)

# 5. Least Winning Clubs in History
@app.route('/api/least-winning')
def least_winning():
    """Fetches data for 'Least Winning Clubs in History'."""
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        club,
        SUM(jg) AS total_wins
    FROM 
        lbf_historical_stats
    GROUP BY 
        club
    ORDER BY 
        total_wins ASC
    LIMIT 10;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    data = [{"club": row[0], "total_wins": row[1]} for row in rows]
    return jsonify(data)

# 6. Clubs with Negative Goal Difference
@app.route('/api/negative-goal-difference')
def negative_goal_difference():
    """Fetches data for 'Clubs with the Most Negative Goal Difference'."""
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        club,
        SUM(dif) AS goal_difference
    FROM 
        lbf_historical_stats
    GROUP BY 
        club
    HAVING 
        SUM(dif) < 0
    ORDER BY 
        goal_difference ASC
    LIMIT 10;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    data = [{"club": row[0], "goal_difference": row[1]} for row in rows]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
