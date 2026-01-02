"""
Componentes de navegación entre páginas
"""
from dash import html
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config.settings import COLORS, PORTS


def create_nav_button(text, port, icon="🔗", gradient_colors=None):
    """
    Crea un botón de navegación
    
    Args:
        text: Texto del botón
        port: Puerto al que navega
        icon: Icono del botón
        gradient_colors: Tupla de (color1, color2) para el gradiente
        
    Returns:
        html.A: Enlace con botón estilizado
    """
    if gradient_colors is None:
        gradient_colors = (COLORS['primary'], COLORS['secondary'])
    
    return html.A([
        html.Button([
            html.Span(icon + " ", style={'margin-right': '8px'}),
            text
        ], style={
            'background': f'linear-gradient(135deg, {gradient_colors[0]} 0%, {gradient_colors[1]} 100%)',
            'border': 'none',
            'color': COLORS['background'],
            'padding': '12px 30px',
            'font-size': '15px',
            'font-weight': '600',
            'border-radius': '10px',
            'cursor': 'pointer',
            'box-shadow': f'0 4px 15px rgba(0, 212, 255, 0.3)',
            'transition': 'transform 0.3s ease',
            'margin-right': '15px'
        })
    ], href=f'http://127.0.0.1:{port}/', target='_blank', style={'text-decoration': 'none'})


def create_navigation_menu():
    """
    Crea el menú de navegación completo
    
    Returns:
        html.Div: Menú de navegación vacío (botones removidos)
    """
    return html.Div([], style={'text-align': 'center', 'margin-bottom': '20px'})


def create_back_button(target_port, text="Volver al Dashboard Principal"):
    """
    Crea un botón de retorno
    
    Args:
        target_port: Puerto al que regresa
        text: Texto del botón
        
    Returns:
        html.Div: Botón de retorno
    """
    return html.Div([
        html.A([
            html.Button([
                html.Span("← ", style={'margin-right': '8px'}),
                text
            ], style={
                'background': f'linear-gradient(135deg, {COLORS["surface"]} 0%, #252b4a 100%)',
                'border': f'2px solid {COLORS["primary"]}',
                'color': COLORS['primary'],
                'padding': '12px 30px',
                'font-size': '15px',
                'font-weight': '600',
                'border-radius': '10px',
                'cursor': 'pointer',
                'transition': 'all 0.3s ease',
            })
        ], href=f'http://127.0.0.1:{target_port}/', target='_blank', style={'text-decoration': 'none'})
    ], style={'text-align': 'center', 'margin-top': '30px'})
