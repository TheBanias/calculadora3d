import sys
import os
import re
import requests
from flask import Flask, render_template, request as flask_request, redirect, url_for, session, jsonify
from datetime import datetime

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

template_dir = os.path.join(base_path, "templates")
static_dir = os.path.join(base_path, "static")

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = "clave-secreta"

# Filtro para convertir timestamp epoch a fecha
@app.template_filter('epoch_to_date')
def epoch_to_date_filter(epoch):
    try:
        return datetime.fromtimestamp(float(epoch)).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return "-"

def get_filamentos():
    return session.get('filamentos', [])

def save_filamentos(filamentos):
    session['filamentos'] = filamentos

def get_impresoras():
    return session.get('impresoras', [])

def save_impresoras(impresoras):
    session['impresoras'] = impresoras

def safe_int(valor):
    try:
        return int(valor)
    except (ValueError, TypeError):
        return 0

def parse_gcode_time(file_stream):
    lines = file_stream.read().decode(errors='ignore').split('\n')
    hours = mins = secs = 0
    for line in lines:
        m = re.search(r'Time: (\d+):(\d+):(\d+)', line)
        if m:
            hours, mins, secs = int(m.group(1)), int(m.group(2)), int(m.group(3))
        m2 = re.search(r';TIME:(\d+)', line)
        if m2:
            total_seconds = int(m2.group(1))
            hours, mins, secs = total_seconds // 3600, (total_seconds % 3600) // 60, total_seconds % 60
    return hours, mins, secs

def moonraker_printer_status(base_url):
    try:
        response = requests.get(f"{base_url}/printer/objects/query", params={"objects": "print_stats"})
        data = response.json()
        stats = data.get("result", {}).get("status", {}).get("print_stats", {})
        return {
            "state": stats.get("state", "desconocido"),
            "print_duration": stats.get("print_duration", 0)
        }
    except Exception as e:
        return {"error": str(e)}

def moonraker_list_jobs(base_url):
    try:
        response = requests.get(f"{base_url}/server/jobs")
        data = response.json()
        jobs = data.get("result", {}).get("jobs", [])
        return jobs
    except Exception as e:
        return []

def moonraker_print_history(base_url):
    try:
        response = requests.get(f"{base_url}/history/list")
        data = response.json()
        if "result" in data and "prints" in data["result"]:
            return data["result"]["prints"]  # Lista de dicts con info de cada impresión
        else:
            return []
    except Exception as e:
        return []

@app.route("/", methods=['GET', 'POST'])
def index():
    filamentos = get_filamentos()
    impresoras = get_impresoras()
    result = None
    printer_status = None
    jobs = None
    selected_job = None
    history = None
    horas = mins = secs = 0

    if flask_request.method == 'POST':
        if 'calcular' in flask_request.form:
            precio_bobina = float(flask_request.form['precio_bobina'])
            peso_pieza = float(flask_request.form['peso_pieza'])
            peso_bobina = float(flask_request.form['peso_bobina'])

            job_seconds = int(flask_request.form.get('job_duration', 0))
            if job_seconds > 0:
                t_total = job_seconds
            else:
                horas = safe_int(flask_request.form.get('horas'))
                mins = safe_int(flask_request.form.get('minutos'))
                secs = safe_int(flask_request.form.get('segundos'))
                t_total = (horas * 3600) + (mins * 60) + secs

                if 'gcode' in flask_request.files:
                    gcode = flask_request.files['gcode']
                    if gcode and gcode.filename.endswith('.gcode'):
                        gh, gm, gs = parse_gcode_time(gcode.stream)
                        if gh + gm + gs > 0:
                            t_total = (gh * 3600) + (gm * 60) + gs

            costo_material = (peso_pieza / peso_bobina) * precio_bobina
            horas_decimales = t_total / 3600

            potencia_kw = 0.12
            coste_kwh = 0.147
            consumo = potencia_kw * horas_decimales
            coste_luz = consumo * coste_kwh

            result = {
                "material": round(costo_material, 2),
                "luz": round(coste_luz, 2),
                "consumo": round(consumo, 3),
                "potencia": int(potencia_kw * 1000),
                "tiempo_h": horas,
                "tiempo_m": mins,
                "tiempo_s": secs,
                "horas_decimales": round(horas_decimales, 2),
                "usado_gcode": 'gcode' in flask_request.files,
                "total": round(costo_material + coste_luz, 2)
            }

        elif 'agregar_impresora' in flask_request.form:
            nombre = flask_request.form['nombre_impresora']
            url = flask_request.form['url_moonraker'].rstrip('/')
            impresoras.append({"nombre": nombre, "url": url})
            save_impresoras(impresoras)
            return redirect(url_for('index'))

        elif 'seleccionar_impresora' in flask_request.form:
            index = int(flask_request.form['impresora_seleccionada'])
            if 0 <= index < len(impresoras):
                url = impresoras[index]["url"]
                printer_status = moonraker_printer_status(url)
                jobs = moonraker_list_jobs(url)
                history = moonraker_print_history(url)
            else:
                history = []

    return render_template("index.html", filamentos=filamentos, impresoras=impresoras,
                           result=result, printer_status=printer_status, jobs=jobs,
                           selected_job=selected_job, enumerate=enumerate, history=history)

@app.route("/agregar_filamento", methods=['GET', 'POST'])
def agregar_filamento():
    filamentos = get_filamentos()
    if flask_request.method == 'POST':
        nombre = flask_request.form['nombre_filamento']
        precio = float(flask_request.form['precio_bobina'])
        peso = float(flask_request.form['peso_bobina'])

        filamentos.append({"nombre": nombre, "precio": precio, "peso": peso})
        save_filamentos(filamentos)
        return redirect(url_for('index'))

    return render_template("agregar_filamento.html")

@app.route("/filamento/<int:index>")
def obtener_filamento(index):
    filamentos = get_filamentos()
    if 0 <= index < len(filamentos):
        return jsonify(filamentos[index])
    return jsonify({}), 404

if __name__ == "__main__":
    app.run(debug=True)
