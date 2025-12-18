"""
Dashboard Avanzado de Fitness - Refactorizado
Heatmaps, tendencias, predicciones y rankings
"""
from dash import Dash
import dash_bootstrap_components as dbc
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from config.settings import COLORS, PORTS
from src.utils.data_loader import load_fitness_data, get_date_range
from src.layouts.advanced_layout import create_advanced_layout
from src.callbacks.advanced_callbacks import register_advanced_callbacks


# HTML personalizado para el date picker
index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .DateInput_input {
                background-color: #1a1f3a !important;
                color: #e0e6f0 !important;
                border: 1px solid rgba(0, 255, 136, 0.3) !important;
                border-radius: 8px !important;
                padding: 8px 12px !important;
                font-size: 14px !important;
            }
            .DateInput_input:focus {
                border-color: #00ff88 !important;
                box-shadow: 0 0 10px rgba(0, 255, 136, 0.3) !important;
            }
            .DateRangePicker_picker {
                z-index: 9999 !important;
                background: #1a1f3a !important;
                border: 2px solid #00ff88 !important;
                border-radius: 12px !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Inicializar aplicación
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True,
    title="Análisis Avanzado - Fitness"
)

app.index_string = index_string

# Cargar datos
print("📊 Cargando datos para análisis avanzado...")
df = load_fitness_data()
print(f"✅ Datos cargados: {len(df)} registros")

# Obtener rango de fechas
first_date, last_date = get_date_range(df)

# Crear layout
app.layout = create_advanced_layout(first_date, last_date)

# Registrar callbacks
register_advanced_callbacks(app, df)

if __name__ == '__main__':
    print(f"\n🚀 Iniciando Dashboard Avanzado en http://127.0.0.1:{PORTS['advanced']}/\n")
    app.run(debug=True, port=PORTS['advanced'])
