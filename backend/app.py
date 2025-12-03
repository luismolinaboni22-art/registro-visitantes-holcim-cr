from flask import Flask, request, jsonify, render_template, send_from_directory
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

DB_PATH = "visitas.db"

# ---------------------- BASE DE DATOS ----------------------

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Tabla de usuarios
        cursor.execute("""
            CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        # Usuario por defecto
        cursor.execute("""
            INSERT INTO usuarios (usuario, password)
            VALUES (?, ?)
        """, ("CoordinadorHolcim", generate_password_hash("123")))

        # Tabla de visitantes
        cursor.execute("""
            CREATE TABLE visitantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                cedula TEXT,
                empresa TEXT,
                persona_visita TEXT,
                motivo TEXT,
                placa TEXT,
                hora_ingreso TEXT,
                hora_salida TEXT
            )
        """)

        conn.commit()
        conn.close()
        print("Base de datos creada correctamente.")

# ---------------------- RUTAS ----------------------

@app.route("/")
def home():
    return send_from_directory("../frontend", "login.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    usuario = data.get("usuario")
    password = data.get("password")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM usuarios WHERE usuario = ?", (usuario,))
    result = cursor.fetchone()
    conn.close()

    if result and check_password_hash(result[0], password):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

@app.route("/registrar", methods=["POST"])
def registrar():
    data = request.json

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO visitantes (nombre, cedula, empresa, persona_visita, motivo, placa, hora_ingreso, hora_salida)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("nombre"),
        data.get("cedula"),
        data.get("empresa"),
        data.get("persona_visita"),
        data.get("motivo"),
        data.get("placa"),
        data.get("hora_ingreso"),
        data.get("hora_salida")
    ))
    conn.commit()
    conn.close()

    return jsonify({"success": True})


# ---------------------- EJECUCIÓN ----------------------

if __name__ == "__main__":
    init_db()

    port = int(os.environ.get("PORT", 5000))
    print(f"➡ Ejecutando en el puerto: {port}")

    app.run(host="0.0.0.0", port=port)


