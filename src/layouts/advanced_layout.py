"""
Layout del dashboard avanzado
"""
from dash import html, dcc
import dash_bootstrap_components as dbc
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config.settings import COLORS, CARD_STYLE
from src.components.cards import create_stat_card
from src.components.navigation import create_back_button, PORTS


def create_advanced_layout(first_date, last_date):
    """Crea el layout del dashboard avanzado"""
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1([
                        html.Span("🚀 ", style={'font-size': '50px'}),
                        "Análisis Avanzado"
                    ], style={
                        'color': COLORS['success'],
                        'font-weight': '700',
                        'margin-bottom': '5px',
                        'text-align': 'center'
                    }),
                    html.P("Heatmaps, tendencias, predicciones y rankings", style={
                        'color': COLORS['text_secondary'],
                        'text-align': 'center',
                        'font-size': '16px',
                        'margin-bottom': '20px'
                    }),
                    create_back_button(PORTS['main'])
                ])
            ])
        ], className='mb-4'),
        
        # Tarjetas de estadísticas
        dbc.Row([
            create_stat_card("👣", "Total Pasos", "adv-total-steps", "adv-avg-steps", "primary"),
            create_stat_card("🏃", "Distancia", "adv-total-distance", "adv-distance-world", "success"),
            create_stat_card("🔥", "Calorías", "adv-total-calories", "adv-avg-calories", "secondary"),
            create_stat_card("⏱️", "Minutos Activos", "adv-total-active-minutes", "adv-active-hours", "warning")
        ], className='mb-4'),
        
        # Filtro de fechas
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label("📅 Filtrar por rango de fechas:", style={
                        'color': COLORS['success'],
                        'font-weight': '600',
                        'margin-bottom': '10px',
                        'font-size': '16px'
                    }),
                    dcc.DatePickerRange(
                        id='adv-date-range',
                        start_date=first_date,
                        end_date=last_date,
                        display_format='DD/MM/YYYY'
                    )
                ], style=CARD_STYLE)
            ])
        ], className='mb-4'),
        
        # Visualizaciones avanzadas
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("📅 Calendario de Actividad (Heatmap)", style={
                        'color': COLORS['success'],
                        'font-size': '20px',
                        'margin-bottom': '15px'
                    }),
                    dcc.Graph(id='heatmap-calendar', config={'displayModeBar': False})
                ], style=CARD_STYLE)
            ])
        ], className='mb-4'),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("⚖️ Evolución del Peso", style={'color': COLORS['success'], 'font-size': '20px', 'margin-bottom': '15px'}),
                    dcc.Graph(id='weight-trend', config={'displayModeBar': False})
                ], style=CARD_STYLE)
            ], xs=12, lg=6),
            dbc.Col([
                html.Div([
                    html.H3("🏃 Análisis de Velocidad y Pace", style={'color': COLORS['success'], 'font-size': '20px', 'margin-bottom': '15px'}),
                    dcc.Graph(id='speed-analysis', config={'displayModeBar': False})
                ], style=CARD_STYLE)
            ], xs=12, lg=6)
        ], className='mb-4'),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("❤️ Frecuencia Cardíaca", style={'color': COLORS['success'], 'font-size': '20px', 'margin-bottom': '15px'}),
                    dcc.Graph(id='heart-rate-analysis', config={'displayModeBar': False})
                ], style=CARD_STYLE)
            ], xs=12, lg=6),
            dbc.Col([
                html.Div([
                    html.H3("📊 Comparativa Año vs Año", style={'color': COLORS['success'], 'font-size': '20px', 'margin-bottom': '15px'}),
                    dcc.Graph(id='year-comparison', config={'displayModeBar': False})
                ], style=CARD_STYLE)
            ], xs=12, lg=6)
        ], className='mb-4'),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("🎯 Progreso hacia Objetivos", style={'color': COLORS['success'], 'font-size': '20px', 'margin-bottom': '15px'}),
                    dcc.Graph(id='goals-progress', config={'displayModeBar': False})
                ], style=CARD_STYLE)
            ])
        ], className='mb-4'),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("🏆 Top 10 Mejores Días", style={'color': COLORS['warning'], 'font-size': '20px', 'margin-bottom': '15px'}),
                    html.Div(id='top-rankings')
                ], style=CARD_STYLE)
            ], xs=12, lg=6),
            dbc.Col([
                html.Div([
                    html.H3("💪 Intensidad de Entrenamiento", style={'color': COLORS['success'], 'font-size': '20px', 'margin-bottom': '15px'}),
                    dcc.Graph(id='intensity-analysis', config={'displayModeBar': False})
                ], style=CARD_STYLE)
            ], xs=12, lg=6)
        ], className='mb-4'),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("🔮 Análisis Predictivo (30 días)", style={'color': COLORS['success'], 'font-size': '20px', 'margin-bottom': '15px'}),
                    dcc.Graph(id='predictive-analysis', config={'displayModeBar': False})
                ], style=CARD_STYLE)
            ])
        ])
        
    ], fluid=True, style={'background': COLORS['background'], 'padding': '30px', 'min-height': '100vh'})
