"""
Dashboard Unificado de Fitness - Google Fit Analytics
Aplicación principal con navegación entre secciones
"""
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import sys
import os

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from config.settings import COLORS, PORTS
from src.utils.data_loader import load_fitness_data, get_date_range
from src.layouts.main_layout import create_main_layout
from src.layouts.advanced_layout import create_advanced_layout
from src.layouts.conclusions_layout import create_conclusions_layout
from src.callbacks.main_callbacks import register_main_callbacks
from src.callbacks.advanced_callbacks import register_advanced_callbacks
from src.callbacks.conclusions_callbacks import register_conclusions_callbacks


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
            .nav-tabs .nav-link {
                background-color: #1a1f3a !important;
                color: #8892ab !important;
                border: 1px solid rgba(0, 212, 255, 0.2) !important;
                margin: 0 5px !important;
                border-radius: 8px 8px 0 0 !important;
                font-weight: 500 !important;
            }
            .nav-tabs .nav-link:hover {
                color: #00d4ff !important;
                border-color: rgba(0, 212, 255, 0.4) !important;
            }
            .nav-tabs .nav-link.active {
                background-color: #0a0e27 !important;
                color: #00d4ff !important;
                border-color: #00d4ff !important;
                border-bottom: 1px solid #0a0e27 !important;
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

# Inicializar la app
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True
)
app.title = "💪 Fitness Dashboard"
app.index_string = index_string

# Cargar datos
df = load_fitness_data()
min_date, max_date = get_date_range(df)

# Establecer rango de fechas por defecto (1 enero 2025 - 31 diciembre 2025)
from datetime import datetime
default_start_date = datetime(2025, 1, 1)
default_end_date = datetime(2025, 12, 31)

# Ajustar si las fechas por defecto están fuera del rango de datos disponibles
if default_start_date < min_date:
    default_start_date = min_date
if default_end_date > max_date:
    default_end_date = max_date

# Layout principal con pestañas
app.layout = dbc.Container([
    # Store compartido para sincronizar fechas entre pestañas
    dcc.Store(id='shared-date-store', data={
        'start_date': default_start_date.strftime('%Y-%m-%d'),
        'end_date': default_end_date.strftime('%Y-%m-%d')
    }),
    
    # Header
    dbc.Row([
        dbc.Col([
            html.H1(
                "💪 Dashboard de Fitness - Google Fit Analytics",
                className="text-center mb-2",
                style={
                    'color': COLORS['primary'],
                    'textShadow': f'0 0 20px {COLORS["primary"]}',
                    'fontWeight': 'bold',
                    'fontSize': '2.5rem',
                    'marginTop': '20px'
                }
            ),
            html.P(
                "Visualiza tus métricas de actividad física de forma interactiva",
                className="text-center text-muted mb-4",
                style={'fontSize': '1.1rem'}
            )
        ])
    ]),
    
    # Navegación por pestañas
    dbc.Row([
        dbc.Col([
            dbc.Tabs(
                id="tabs",
                active_tab="tab-principal",
                children=[
                    dbc.Tab(
                        label="🏠 Dashboard Principal",
                        tab_id="tab-principal",
                        label_style={'fontSize': '1.1rem', 'padding': '12px 24px'}
                    ),
                    dbc.Tab(
                        label="🚀 Análisis Avanzado",
                        tab_id="tab-avanzado",
                        label_style={'fontSize': '1.1rem', 'padding': '12px 24px'}
                    ),
                    dbc.Tab(
                        label="🎯 Conclusiones",
                        tab_id="tab-conclusiones",
                        label_style={'fontSize': '1.1rem', 'padding': '12px 24px'}
                    ),
                ],
                style={'marginBottom': '20px'}
            )
        ])
    ]),
    
    # Contenido dinámico
    html.Div(id="tab-content", style={'marginTop': '20px'})
    
], fluid=True, style={
    'backgroundColor': COLORS['background'],
    'minHeight': '100vh',
    'padding': '20px'
})


# Callback para cambiar el contenido según la pestaña
@callback(
    Output('tab-content', 'children'),
    Input('tabs', 'active_tab')
)
def render_tab_content(active_tab):
    # Calcular días activos
    total_days = len(df[df['Recuento de pasos'] > 0])
    
    if active_tab == "tab-principal":
        return create_main_layout(default_start_date, default_end_date, total_days)
    elif active_tab == "tab-avanzado":
        return create_advanced_layout(default_start_date, default_end_date)
    elif active_tab == "tab-conclusiones":
        from src.utils.data_loader import filter_data_by_date
        filtered_df = filter_data_by_date(df, default_start_date, default_end_date)
        return create_conclusions_layout(default_start_date, default_end_date, filtered_df)
    return html.Div("Selecciona una pestaña")


# Registrar callbacks de cada sección
register_main_callbacks(app, df)
register_advanced_callbacks(app, df)
register_conclusions_callbacks(app, df)


# Servidor para producción
server = app.server

if __name__ == '__main__':
    import os
    print("=" * 60)
    print("💪 Iniciando Dashboard de Fitness")
    print("=" * 60)
    
    # Detectar si estamos en producción o desarrollo
    is_production = os.environ.get('RENDER') is not None
    
    if is_production:
        # Render usará gunicorn automáticamente
        port = int(os.environ.get('PORT', 10000))
        print(f"🌐 Modo producción - Puerto: {port}")
    else:
        print(f"🌐 Abriendo en: http://127.0.0.1:{PORTS['main']}/")
        print("=" * 60)
        app.run_server(
            debug=True,
            host='127.0.0.1',
            port=PORTS['main']
        )
