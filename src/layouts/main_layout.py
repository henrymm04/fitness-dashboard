"""
Layout del dashboard principal
"""
from dash import html, dcc
import dash_bootstrap_components as dbc
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config.settings import COLORS, CARD_STYLE
from src.components.cards import create_stat_card
from src.components.navigation import create_navigation_menu


def create_main_layout(first_date, last_date, total_days):
    """
    Crea el layout del dashboard principal
    
    Args:
        first_date: Primera fecha de datos
        last_date: Última fecha de datos
        total_days: Total de días activos
        
    Returns:
        dbc.Container: Layout completo
    """
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1([
                        html.Span("💪 ", style={'font-size': '50px'}),
                        "Dashboard de Fitness"
                    ], style={
                        'color': COLORS['primary'],
                        'font-weight': '700',
                        'margin-bottom': '5px',
                        'text-align': 'center',
                        'font-family': 'Segoe UI, sans-serif'
                    }),
                    html.P([
                        f"📊 Datos desde {first_date.strftime('%d/%m/%Y')} hasta {last_date.strftime('%d/%m/%Y')} ({total_days} días activos)"
                    ], style={
                        'color': COLORS['text_secondary'],
                        'text-align': 'center',
                        'font-size': '16px',
                        'margin-bottom': '20px'
                    }),
                    create_navigation_menu()
                ])
            ])
        ], className='mb-4'),
        
        # Tarjetas de estadísticas
        dbc.Row([
            create_stat_card("👣", "Total Pasos", "total-steps", "avg-steps", "primary"),
            create_stat_card("🏃", "Distancia", "total-distance", "distance-world", "success"),
            create_stat_card("🔥", "Calorías", "total-calories", "avg-calories", "secondary"),
            create_stat_card("⏱️", "Minutos Activos", "total-active-minutes", "active-hours", "warning")
        ], className='mb-4'),
        
        # Filtro de fechas
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label("📅 Filtrar por rango de fechas:", style={
                        'color': COLORS['primary'],
                        'font-weight': '600',
                        'margin-bottom': '10px',
                        'font-size': '16px'
                    }),
                    dcc.DatePickerRange(
                        id='date-range',
                        start_date=first_date,
                        end_date=last_date,
                        display_format='DD/MM/YYYY',
                        style={'width': '100%'}
                    )
                ], style=CARD_STYLE)
            ])
        ], className='mb-4'),
        
        # Gráficos principales
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("📈 Evolución de Pasos Diarios", style={
                        'color': COLORS['primary'],
                        'font-size': '20px',
                        'margin-bottom': '15px'
                    }),
                    dcc.Graph(id='steps-trend', config={'displayModeBar': False})
                ], style=CARD_STYLE)
            ], xs=12, lg=8),
            dbc.Col([
                html.Div([
                    html.H3("📊 Distribución de Actividad", style={
                        'color': COLORS['primary'],
                        'font-size': '20px',
                        'margin-bottom': '15px'
                    }),
                    dcc.Graph(id='activity-distribution', config={'displayModeBar': False})
                ], style=CARD_STYLE)
            ], xs=12, lg=4)
        ], className='mb-4'),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("📅 Métricas Mensuales", style={
                        'color': COLORS['primary'],
                        'font-size': '20px',
                        'margin-bottom': '15px'
                    }),
                    dcc.Graph(id='monthly-metrics', config={'displayModeBar': False})
                ], style=CARD_STYLE)
            ], xs=12, lg=6),
            dbc.Col([
                html.Div([
                    html.H3("🗓️ Actividad por Día de la Semana", style={
                        'color': COLORS['primary'],
                        'font-size': '20px',
                        'margin-bottom': '15px'
                    }),
                    dcc.Graph(id='weekday-activity', config={'displayModeBar': False})
                ], style=CARD_STYLE)
            ], xs=12, lg=6)
        ], className='mb-4'),
        
        # Tabla jerárquica
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("📋 Resumen Jerárquico por Año y Mes", style={
                        'color': COLORS['primary'],
                        'font-size': '20px',
                        'margin-bottom': '15px'
                    }),
                    html.Div(id='hierarchical-table')
                ], style=CARD_STYLE)
            ])
        ])
        
    ], fluid=True, style={'background': COLORS['background'], 'padding': '30px', 'min-height': '100vh'})
