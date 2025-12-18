"""
Dashboard Principal de Fitness - Refactorizado
Aplicación modular con arquitectura limpia
"""
from dash import Dash
import dash_bootstrap_components as dbc
import sys
import os

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from config.settings import COLORS, PORTS
from src.utils.data_loader import load_fitness_data, get_date_range, calculate_summary_stats
from src.layouts.main_layout import create_main_layout
from src.callbacks.main_callbacks import register_main_callbacks


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
                border: 1px solid rgba(0, 212, 255, 0.3) !important;
                border-radius: 8px !important;
                padding: 8px 12px !important;
                font-size: 14px !important;
            }
            .DateInput_input:focus {
                border-color: #00d4ff !important;
                box-shadow: 0 0 10px rgba(0, 212, 255, 0.3) !important;
            }
            .DateInput_input::placeholder {
                color: #8892ab !important;
            }
            .DateRangePickerInput {
                background-color: transparent !important;
                border: none !important;
            }
            .DateRangePickerInput_arrow {
                color: #00d4ff !important;
            }
            .CalendarMonth_caption {
                color: #00d4ff !important;
                font-weight: 600 !important;
            }
            .DayPicker {
                background: #1a1f3a !important;
            }
            .CalendarDay {
                border: 1px solid rgba(255,255,255,0.1) !important;
                color: #e0e6f0 !important;
            }
            .CalendarDay__default:hover {
                background: rgba(0, 212, 255, 0.2) !important;
                border: 1px solid #00d4ff !important;
            }
            .DayPickerNavigation_button {
                border: 1px solid rgba(0, 212, 255, 0.3) !important;
            }
            .DayPickerNavigation_svg__horizontal {
                fill: #00d4ff !important;
            }
            .DateRangePicker {
                z-index: 9999 !important;
            }
            .DateRangePicker_picker {
                z-index: 9999 !important;
                background: #1a1f3a !important;
                border: 2px solid #00d4ff !important;
                border-radius: 12px !important;
                box-shadow: 0 10px 40px rgba(0, 212, 255, 0.3) !important;
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

# Inicializar la aplicación
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True,
    title="Dashboard de Fitness"
)

app.index_string = index_string

# Cargar datos
print("📊 Cargando datos...")
df = load_fitness_data()
print(f"✅ Datos cargados: {len(df)} registros")

# Obtener información de fechas
first_date, last_date = get_date_range(df)
stats = calculate_summary_stats(df)

print(f"📅 Rango: {first_date.strftime('%d/%m/%Y')} - {last_date.strftime('%d/%m/%Y')}")
print(f"👣 Total de pasos: {stats['total_steps']:,}")

# Crear layout
app.layout = create_main_layout(first_date, last_date, stats['active_days'])

# Registrar callbacks
register_main_callbacks(app, df)

if __name__ == '__main__':
    print(f"\n🚀 Iniciando Dashboard Principal en http://127.0.0.1:{PORTS['main']}/\n")
    app.run(debug=True, port=PORTS['main'])
