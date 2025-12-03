from flask import Flask, request, jsonify, session, redirect, url_for, send_from_directory, g
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "visitors.db"

app = Flask(__name__, static_folder=str(BASE_DIR.parent / 'frontend' / 'static'), static_url_path='/static')
app.secret_key = 'cambiar_esto_por_una_clave_mas_segura'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(BASE_DIR / "data", exist_ok=True)
    if not DB_PATH.exists():
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        ''')
        cur.execute('''
            CREATE TABLE visitors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                cedula TEXT,
                empresa TEXT,
                persona_visitada TEXT,
                motivo TEXT,
                placa TEXT,
                hora_ingreso TEXT,
                hora_salida TEXT
            );
        ''')
        # Default user: CoordinadorHolcim / 123
        hashed = generate_password_hash("123")
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("CoordinadorHolcim", hashed))
        conn.commit()
        conn.close()

@app.before_request
def open_db():
    g.db = get_db()

@app.teardown_request
def close_db(exc):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def root():
    return send_from_directory(str(BASE_DIR.parent / 'frontend'), 'login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    cur = g.db.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    if user and check_password_hash(user['password'], password):
        session['user'] = username
        return jsonify({"ok": True, "msg": "Login successful"})
    return jsonify({"ok": False, "msg": "Credenciales inválidas"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"ok": True})

def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get('user') is None:
            return jsonify({"ok": False, "msg": "No autorizado"}), 401
        return f(*args, **kwargs)
    return wrapper

@app.route('/register_visitor', methods=['POST'])
@login_required
def register_visitor():
    data = request.get_json() or {}
    fields = ("nombre","cedula","empresa","persona_visitada","motivo","placa","hora_ingreso","hora_salida")
    values = [data.get(f,"") for f in fields]
    cur = g.db.cursor()
    cur.execute('''
        INSERT INTO visitors (nombre,cedula,empresa,persona_visitada,motivo,placa,hora_ingreso,hora_salida)
        VALUES (?,?,?,?,?,?,?,?);
    ''', values)
    g.db.commit()
    return jsonify({"ok": True, "msg": "Visitante registrado"})

@app.route('/visitors', methods=['GET'])
@login_required
def visitors():
    cur = g.db.execute("SELECT * FROM visitors ORDER BY id DESC")
    rows = [dict(r) for r in cur.fetchall()]
    return jsonify(rows)

# serve frontend files (index.html and login.html)
@app.route('/<path:filename>')
def frontend_files(filename):
    ff = BASE_DIR.parent / 'frontend' / filename
    if ff.exists():
        return send_from_directory(str(BASE_DIR.parent / 'frontend'), filename)
    else:
        return "File not found", 404

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

