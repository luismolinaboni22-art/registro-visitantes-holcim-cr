from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Base de datos temporal en memoria
visitantes = []

@app.route('/')
def index():
    return render_template("index.html", visitantes=visitantes)

@app.route('/agregar', methods=['POST'])
def agregar():
    visitante = {
        "nombre": request.form['nombre'],
        "cedula": request.form['cedula'],
        "empresa": request.form['empresa'],
        "persona_visita": request.form['persona_visita'],
        "motivo": request.form['motivo'],
        "placa": request.form['placa'],
        "hora_ingreso": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "hora_salida": ""
    }

    visitantes.append(visitante)
    return redirect(url_for('index'))

@app.route('/salida/<int:id>')
def salida(id):
    visitantes[id]["hora_salida"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)


