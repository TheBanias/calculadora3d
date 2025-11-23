# Calculadora de Costos de Impresión 3D

Proyecto web para calcular el coste total de piezas impresas en 3D, con integración a Moonraker/Klipper para consultar trabajos activos y el historial de impresiones realizadas. Permite guardar filamentos favoritos, agregar impresoras y calcular automáticamente el gasto energético y de material.

## Características

- **Calcula el coste de impresión 3D:** considera tanto el material como el gasto eléctrico (precio medio de España).
- **Gestión de filamentos:** selección rápida de filamentos y opción para añadir composiciones personalizadas.
- **Integración con Moonraker/Klipper:** agrega impresoras, consulta el estado actual y muestra trabajos activos.
- **Historial y trabajos activos:** visualiza el historial de impresiones realizadas (requiere Moonraker con el módulo `[history]`) y selecciona un trabajo activo para usar sus tiempos.
- **Interfaz responsive y fácil de usar.**

---

## Instalación y uso

### Requisitos

- Python 3.8 o superior
- Flask, requests, PyInstaller (opcional)
- Acceso a una impresora con Klipper y Moonraker

### Instalación

```bash
git clone https://github.com/rohanini/calculadora3d.git
cd calculadora3d
python -m venv env
source env/Scripts/activate  # En Windows usa: env\Scripts\activate
pip install flask requests
```

### Ejecución en desarrollo

```bash
python app.py
```

Luego, accede a [http://127.0.0.1:5000/](http://127.0.0.1:5000/) en tu navegador.
