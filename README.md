Calculadora de Costos de Impresión 3D
Proyecto web para calcular el coste total de piezas impresas en 3D, con integración a Moonraker/Klipper para consulta de trabajos activos y el historial de impresiones realizadas.
Permite guardar filamentos favoritos, agregar impresoras y calcular automáticamente el gasto energético/material.

Características
Calcula el coste de impresión 3D: material y luz (precio medio España).

Selección rápida de filamentos y creación personalizada.

Agrega impresoras Moonraker y consulta estado actual.

Visualiza trabajos activos y selecciona uno para usar sus tiempos.

Muestra el historial de impresiones realizadas (requiere Moonraker [history]).

Interfaz responsive y fácil de usar.




Instalación y uso
Requisitos
Python 3.8+

Flask, requests, PyInstaller (opcional)

Acceso a una impresora con Klipper + Moonraker

Instalación
bash
git clone https://github.com/tunombre/calculadora3d.git
cd calculadora3d
python -m venv env
source env/Scripts/activate
pip install flask requests
Ejecutar en desarrollo
bash
python app.py
Accede a http://127.0.0.1:5000/ en tu navegador.