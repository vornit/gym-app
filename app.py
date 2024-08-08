from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workout_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                exercise TEXT NOT NULL,
                set1 INTEGER NOT NULL,
                set2 INTEGER NOT NULL,
                set3 INTEGER NOT NULL,
                FOREIGN KEY (session_id) REFERENCES workout_sessions(id)
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/history')
def history():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.timestamp, w.exercise, w.set1, w.set2, w.set3
            FROM workout_sessions s
            JOIN workouts w ON s.id = w.session_id
            ORDER BY s.timestamp
        ''')
        workouts = cursor.fetchall()
    return render_template('history.html', workouts=workouts)

@app.route('/add_workout', methods=['POST'])
def add_workout():
    timestamp = request.form['timestamp']
    workout_data = {
        'bench_set1': request.form['bench_set1'],
        'bench_set2': request.form['bench_set2'],
        'bench_set3': request.form['bench_set3'],
        'squat_set1': request.form['squat_set1'],
        'squat_set2': request.form['squat_set2'],
        'squat_set3': request.form['squat_set3']
    }
    
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO workout_sessions (timestamp) VALUES (?)
        ''', (timestamp,))
        session_id = cursor.lastrowid
        cursor.execute('''
            INSERT INTO workouts (session_id, exercise, set1, set2, set3) VALUES
            (?, ?, ?, ?, ?), (?, ?, ?, ?, ?)
        ''', (
            session_id, 'Bench', workout_data['bench_set1'], workout_data['bench_set2'], workout_data['bench_set3'],
            session_id, 'Squat', workout_data['squat_set1'], workout_data['squat_set2'], workout_data['squat_set3']
        ))
        conn.commit()
    return jsonify({'status': 'success'})

@app.route('/get_workouts', methods=['GET'])
def get_workouts():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.timestamp, w.exercise, w.set1, w.set2, w.set3
            FROM workout_sessions s
            JOIN workouts w ON s.id = w.session_id
            ORDER BY s.timestamp
        ''')
        workouts = cursor.fetchall()
    return jsonify([{
        'timestamp': workout[0],
        'exercise': workout[1],
        'set1': workout[2],
        'set2': workout[3],
        'set3': workout[4]
    } for workout in workouts])

if __name__ == '__main__':
    init_db()  # Initialize the database if it does not exist
    app.run(debug=True)
