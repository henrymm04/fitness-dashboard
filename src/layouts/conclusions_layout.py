"""
Layout de Conclusiones
Análisis detallado y hallazgos clave
"""
from dash import html
import dash_bootstrap_components as dbc
from config.settings import COLORS


def create_conclusions_layout(df):
    """
    Crea el layout de conclusiones con análisis detallado
    
    Args:
        df: DataFrame con los datos de fitness
        
    Returns:
        Layout de Dash con las conclusiones
    """
    # Filtrar datos activos
    df_activo = df[df['Recuento de pasos'] > 0].copy()
    
    # Estilos
    conclusion_card = {
        'background': f'linear-gradient(135deg, {COLORS["surface"]} 0%, #252b4a 100%)',
        'border-radius': '20px',
        'padding': '30px',
        'box-shadow': '0 8px 32px 0 rgba(0, 212, 255, 0.1)',
        'border': f'1px solid rgba(0, 212, 255, 0.18)',
        'margin-bottom': '20px'
    }
    
    # Calcular estadísticas
    total_pasos = df['Recuento de pasos'].sum()
    total_distancia = (df['Distancia (m)'].sum() / 1000)
    total_calorias = df['Calorías (kcal)'].sum()
    total_activos = df['Recuento de Minutos Activos'].sum()
    promedio_pasos = df_activo['Recuento de pasos'].mean()
    dias_activos = len(df_activo)
    total_dias = (df['Fecha'].max() - df['Fecha'].min()).days
    
    layout = html.Div([
        # Resumen Ejecutivo
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("📊 Resumen Ejecutivo", 
                           style={'color': COLORS['primary'], 'margin-bottom': '20px'}),
                    html.P([
                        f"Has registrado casi 7 años completos de actividad física con una ",
                        html.Strong(f"consistencia excepcional del {dias_activos/total_dias*100:.1f}%", 
                                   style={'color': COLORS['success']}),
                        " de días activos. ¡Esto demuestra un compromiso impresionante con tu salud!"
                    ], style={'color': COLORS['text'], 'font-size': '16px', 'line-height': '1.8'}),
                    html.Hr(style={'border-color': 'rgba(0, 212, 255, 0.3)', 'margin': '20px 0'}),
                    html.Ul([
                        html.Li([html.Strong(f"{int(total_pasos):,} pasos totales", 
                                           style={'color': COLORS['primary']})]),
                        html.Li([html.Strong(f"{total_distancia:,.1f} km recorridos", 
                                           style={'color': COLORS['success']}), 
                                f" ({total_distancia/40075*100:.2f}% de la vuelta al mundo)"]),
                        html.Li([html.Strong(f"{int(total_calorias):,} kcal quemadas", 
                                           style={'color': COLORS['secondary']})]),
                        html.Li([html.Strong(f"{int(total_activos/60):,} horas de actividad", 
                                           style={'color': COLORS['warning']}), 
                                " física registrada"])
                    ], style={'color': COLORS['text'], 'font-size': '15px', 'line-height': '2'})
                ], style=conclusion_card)
            ])
        ]),
        
        # Hallazgos Clave
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("🎯 Hallazgos Clave", 
                           style={'color': COLORS['primary'], 'margin-bottom': '20px'}),
                    
                    # Logros
                    html.H5("1️⃣ Logros Destacados", 
                           style={'color': COLORS['success'], 'margin-top': '20px'}),
                    html.Ul([
                        html.Li([html.Strong("Consistencia: "), 
                                f"{dias_activos} días activos de {total_dias} días totales"]),
                        html.Li([html.Strong("Promedio actual: "), 
                                f"{promedio_pasos:,.0f} pasos por día"]),
                        html.Li([html.Strong("Total recorrido: "), 
                                f"{total_distancia:,.1f} km"]),
                    ], style={'color': COLORS['text'], 'line-height': '2'}),
                    
                    # Distribución de ejercicios
                    html.H5("2️⃣ Distribución de Actividades", 
                           style={'color': COLORS['warning'], 'margin-top': '30px'}),
                    html.P("Tu rutina está enfocada principalmente en caminar, con oportunidades para diversificar.",
                          style={'color': COLORS['text'], 'line-height': '1.8'}),
                    
                ], style=conclusion_card)
            ], width=12)
        ]),
        
        # Recomendaciones
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("💪 Recomendaciones", 
                           style={'color': COLORS['success'], 'margin-bottom': '20px'}),
                    
                    html.Div([
                        html.H5("1. Mantén la consistencia", 
                               style={'color': COLORS['primary']}),
                        html.P(f"Tu tasa de actividad del {dias_activos/total_dias*100:.1f}% es excelente. ¡Sigue así!"),
                    ], style={'margin-bottom': '25px'}),
                    
                    html.Div([
                        html.H5("2. Objetivo OMS (10,000 pasos/día)", 
                               style={'color': COLORS['primary']}),
                        html.P(f"Promedio actual: {promedio_pasos:,.0f} pasos/día"),
                        html.P("💡 Intenta agregar caminatas cortas durante el día", 
                              style={'font-style': 'italic', 'color': COLORS['text_secondary']}),
                    ], style={'margin-bottom': '25px'}),
                    
                    html.Div([
                        html.H5("3. Diversifica tu entrenamiento", 
                               style={'color': COLORS['primary']}),
                        html.P("Considera agregar ejercicios de fuerza y otras actividades cardiovasculares"),
                    ], style={'margin-bottom': '25px'}),
                    
                ], style={**conclusion_card, 'color': COLORS['text']})
            ], width=12)
        ]),
        
        # Conclusión Final
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("🎉 Conclusión Final", 
                           style={'color': COLORS['primary'], 'margin-bottom': '20px', 
                                 'text-align': 'center'}),
                    html.P([
                        "Tienes una ",
                        html.Strong("trayectoria excepcional", style={'color': COLORS['success']}),
                        " con ",
                        html.Strong(f"{int(total_pasos):,} pasos totales", 
                                  style={'color': COLORS['primary']}),
                        " y una ",
                        html.Strong(f"consistencia del {dias_activos/total_dias*100:.1f}%", 
                                  style={'color': COLORS['warning']}),
                        ". Continúa con tu rutina y considera agregar más variedad para un fitness completo."
                    ], style={'font-size': '18px', 'line-height': '1.8', 
                             'text-align': 'center', 'color': COLORS['text']}),
                    html.H2("¡Sigue así, estás haciendo un gran trabajo! 💪", 
                           style={'color': COLORS['secondary'], 'text-align': 'center', 
                                 'margin-top': '30px', 'font-weight': 'bold'})
                ], style={
                    **conclusion_card, 
                    'background': f'linear-gradient(135deg, rgba(0, 212, 255, 0.15) 0%, rgba(0, 255, 136, 0.15) 100%)', 
                    'border': f'2px solid {COLORS["primary"]}'
                })
            ], width=12)
        ]),
    ])
    
    return layout
