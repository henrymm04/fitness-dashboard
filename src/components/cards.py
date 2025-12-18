"""
Componentes de tarjetas (cards) reutilizables
"""
from dash import html
import dash_bootstrap_components as dbc
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config.settings import STAT_CARD_STYLE, COLORS


def create_stat_card(icon, title, value_id, detail_id, color='primary'):
    """
    Crea una tarjeta de estadística
    
    Args:
        icon: Emoji o icono a mostrar
        title: Título de la estadística
        value_id: ID para el valor principal
        detail_id: ID para el detalle secundario
        color: Color del tema ('primary', 'secondary', 'success', 'warning')
        
    Returns:
        dbc.Col: Columna con la tarjeta
    """
    return dbc.Col([
        html.Div([
            html.Div([
                html.Span(icon, style={
                    'font-size': '40px',
                    'margin-bottom': '10px',
                    'display': 'block'
                }),
                html.H3(title, style={
                    'color': COLORS[color],
                    'font-size': '14px',
                    'font-weight': '600',
                    'margin-bottom': '10px',
                    'text-transform': 'uppercase',
                    'letter-spacing': '1px'
                }),
                html.H2(id=value_id, children="...", style={
                    'color': COLORS['text'],
                    'font-size': '28px',
                    'font-weight': '700',
                    'margin-bottom': '5px'
                }),
                html.P(id=detail_id, children="...", style={
                    'color': COLORS['text_secondary'],
                    'font-size': '13px',
                    'margin': '0'
                })
            ])
        ], style=STAT_CARD_STYLE)
    ], xs=12, sm=6, md=6, lg=3)


def create_info_card(title, content, icon="ℹ️"):
    """
    Crea una tarjeta de información
    
    Args:
        title: Título de la tarjeta
        content: Contenido de la tarjeta
        icon: Icono a mostrar
        
    Returns:
        html.Div: Tarjeta de información
    """
    from config.settings import CARD_STYLE
    
    return html.Div([
        html.H3([
            html.Span(icon, style={'margin-right': '10px'}),
            title
        ], style={
            'color': COLORS['primary'],
            'font-size': '22px',
            'font-weight': '600',
            'margin-bottom': '15px'
        }),
        html.Div(content, style={
            'color': COLORS['text'],
            'font-size': '15px',
            'line-height': '1.6'
        })
    ], style=CARD_STYLE)
