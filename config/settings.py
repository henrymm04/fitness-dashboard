"""
Configuración global del dashboard de fitness
"""
import os

# Ruta al archivo CSV de datos
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'Daily activity metrics.csv')

# Puertos de los servidores
PORTS = {
    'main': 8050,
    'conclusions': 8051,
    'advanced': 8052
}

# Paleta de colores del dashboard
COLORS = {
    'background': '#0a0e27',
    'surface': '#1a1f3a',
    'primary': '#00d4ff',
    'secondary': '#ff6b9d',
    'success': '#00ff88',
    'warning': '#ffd93d',
    'text': '#e0e6f0',
    'text_secondary': '#8892ab'
}

# Objetivos de fitness
GOALS = {
    'daily_steps': 10000,
    'daily_distance': 5,  # km
    'daily_calories': 2000
}

# Configuración de visualizaciones
CHART_CONFIG = {
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'font': {'color': COLORS['text']},
    'margin': {'l': 0, 'r': 0, 't': 0, 'b': 0}
}

# Estilos de componentes
CARD_STYLE = {
    'background': f'linear-gradient(135deg, {COLORS["surface"]} 0%, #252b4a 100%)',
    'border-radius': '20px',
    'padding': '25px',
    'box-shadow': '0 8px 32px 0 rgba(0, 212, 255, 0.1)',
    'border': f'1px solid rgba(0, 212, 255, 0.18)',
    'backdrop-filter': 'blur(10px)',
    'margin-bottom': '20px'
}

STAT_CARD_STYLE = {
    'background': f'linear-gradient(135deg, {COLORS["surface"]} 0%, #252b4a 100%)',
    'border-radius': '20px',
    'padding': '20px',
    'text-align': 'center',
    'box-shadow': '0 8px 32px 0 rgba(0, 212, 255, 0.15)',
    'border': f'1px solid rgba(0, 212, 255, 0.18)',
    'transition': 'transform 0.3s ease',
    'height': '100%'
}
