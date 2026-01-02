"""
Layout de Conclusiones
Análisis detallado y hallazgos clave
"""
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from config.settings import COLORS, CARD_STYLE


def create_conclusions_layout(first_date, last_date, df=None):
    """
    Crea el layout de conclusiones con análisis detallado
    
    Args:
        first_date: Fecha inicial del filtro
        last_date: Fecha final del filtro
        df: DataFrame con los datos (opcional, para contenido inicial)
        
    Returns:
        Layout de Dash con las conclusiones
    """
    # Convertir Pandas Timestamp a datetime si es necesario
    if hasattr(first_date, 'to_pydatetime'):
        first_date = first_date.to_pydatetime()
    if hasattr(last_date, 'to_pydatetime'):
        last_date = last_date.to_pydatetime()
    
    # Estilos
    conclusion_card = {
        'background': f'linear-gradient(135deg, {COLORS["surface"]} 0%, #252b4a 100%)',
        'border-radius': '20px',
        'padding': '30px',
        'box-shadow': '0 8px 32px 0 rgba(0, 212, 255, 0.1)',
        'border': f'1px solid rgba(0, 212, 255, 0.18)',
        'margin-bottom': '20px'
    }
    
    layout = html.Div([
        # Header con filtro de fechas
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1([
                        html.Span("🎯 ", style={'font-size': '50px'}),
                        "Conclusiones y Análisis"
                    ], style={
                        'color': COLORS['primary'],
                        'font-weight': '700',
                        'margin-bottom': '5px',
                        'text-align': 'center'
                    })
                ])
            ])
        ], className='mb-4'),
        
        # Filtro de fechas
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label("📅 Filtrar conclusiones por rango de fechas:", style={
                        'color': COLORS['primary'],
                        'font-weight': '600',
                        'margin-bottom': '10px',
                        'font-size': '16px'
                    }),
                    dcc.DatePickerRange(
                        id='conclusions-date-range',
                        start_date=first_date,
                        end_date=last_date,
                        display_format='DD/MM/YYYY',
                        style={'width': '100%'}
                    )
                ], style={**CARD_STYLE, 'position': 'relative', 'z-index': '1000'})
            ])
        ], className='mb-4', style={'position': 'relative', 'z-index': '1000'}),
        
        # Contenido dinámico - generar contenido inicial si hay datos
        html.Div(
            id='conclusions-content',
            children=create_conclusions_content(df) if df is not None else html.Div("Cargando datos...")
        )
    ])
    
    return layout


def create_conclusions_content(df):
    """
    Crea el contenido dinámico de conclusiones basado en datos filtrados
    
    Args:
        df: DataFrame filtrado con los datos de fitness
        
    Returns:
        Layout con las estadísticas y conclusiones
    """
    # Mapeo de nombres de columnas (por si vienen en inglés o español)
    col_mapping = {
        'pasos': ['Recuento de pasos', 'Step count', 'pasos', 'steps'],
        'distancia': ['Distancia_km', 'Distancia (m)', 'Distance (m)', 'distance'],
        'calorias': ['Calorías (kcal)', 'Calories (kcal)', 'calorias', 'calories'],
        'activos': ['Recuento de Minutos Activos', 'Move Minutes count', 'Active minutes count', 'active_minutes'],
        'fecha': ['Fecha', 'Date', 'fecha', 'date']
    }
    
    # Función para encontrar la columna correcta
    def find_column(df, possible_names):
        for name in possible_names:
            if name in df.columns:
                return name
        return None
    
    # Filtrar datos activos
    col_pasos = find_column(df, col_mapping['pasos'])
    if col_pasos:
        df_activo = df[df[col_pasos] > 0].copy()
    else:
        df_activo = df.copy()
    
    conclusion_card = {
        'background': f'linear-gradient(135deg, {COLORS["surface"]} 0%, #252b4a 100%)',
        'border-radius': '20px',
        'padding': '30px',
        'box-shadow': '0 8px 32px 0 rgba(0, 212, 255, 0.1)',
        'border': f'1px solid rgba(0, 212, 255, 0.18)',
        'margin-bottom': '20px'
    }
    
    # Calcular estadísticas con manejo de errores
    try:
        # Encontrar columnas correctas
        col_pasos = find_column(df, col_mapping['pasos'])
        col_distancia = find_column(df, col_mapping['distancia'])
        col_calorias = find_column(df, col_mapping['calorias'])
        col_activos = find_column(df, col_mapping['activos'])
        col_fecha = find_column(df, col_mapping['fecha'])
        
        # Calcular total de pasos
        if col_pasos and len(df) > 0:
            total_pasos_raw = df[col_pasos].sum()
            # Convertir a Python int/float directamente
            total_pasos = int(float(total_pasos_raw)) if not pd.isna(total_pasos_raw) else 0
        else:
            total_pasos = 0
            
        # Calcular distancia
        if col_distancia and len(df) > 0:
            total_distancia_raw = df[col_distancia].sum()
            # Si la columna es en metros, convertir a km
            if 'Distance (m)' in col_distancia or 'Distancia (m)' in col_distancia:
                total_distancia_raw = total_distancia_raw / 1000
            total_distancia = float(total_distancia_raw) if not pd.isna(total_distancia_raw) else 0.0
        else:
            total_distancia = 0.0
            
        # Calcular calorías
        if col_calorias and len(df) > 0:
            total_calorias_raw = df[col_calorias].sum()
            total_calorias = int(float(total_calorias_raw)) if not pd.isna(total_calorias_raw) else 0
        else:
            total_calorias = 0
            
        # Calcular minutos activos
        if col_activos and len(df) > 0:
            total_activos_raw = df[col_activos].sum()
            total_activos = float(total_activos_raw) if not pd.isna(total_activos_raw) else 0.0
        else:
            total_activos = 0.0
            
    except (ValueError, TypeError, KeyError, AttributeError) as e:
        total_pasos = 0
        total_distancia = 0.0
        total_calorias = 0
        total_activos = 0.0
    
    # Manejar valores NaN o cero
    total_activos_valor = total_activos if isinstance(total_activos, (int, float)) else 0
    if total_activos_valor == 0:
        horas_activas = 0
    else:
        horas_activas = int(total_activos_valor / 60)
    
    # Calcular promedio de pasos de forma segura
    if len(df_activo) > 0 and col_pasos and col_pasos in df_activo.columns:
        promedio_pasos_raw = df_activo[col_pasos].mean()
        promedio_pasos = float(promedio_pasos_raw) if not pd.isna(promedio_pasos_raw) else 0.0
    else:
        promedio_pasos = 0.0
        
    dias_activos = len(df_activo)
    
    # Calcular total de días de forma segura
    if len(df) > 0 and col_fecha and col_fecha in df.columns:
        fecha_min = df[col_fecha].min()
        fecha_max = df[col_fecha].max()
        
        # Convertir a datetime si es necesario
        if hasattr(fecha_min, 'to_pydatetime'):
            fecha_min = fecha_min.to_pydatetime()
        if hasattr(fecha_max, 'to_pydatetime'):
            fecha_max = fecha_max.to_pydatetime()
            
        if fecha_min is not None and fecha_max is not None:
            total_dias = max((fecha_max - fecha_min).days + 1, 1)
        else:
            total_dias = 1
    else:
        total_dias = 1
    
    # Calcular años y porcentaje de días activos
    años_registro = total_dias / 365.25
    porcentaje_consistencia = (dias_activos/total_dias*100) if total_dias > 0 else 0
    
    # Determinar mensaje de consistencia
    if porcentaje_consistencia >= 80:
        mensaje_consistencia = "consistencia excepcional"
        emoji_consistencia = "🌟"
    elif porcentaje_consistencia >= 60:
        mensaje_consistencia = "consistencia notable"
        emoji_consistencia = "👏"
    elif porcentaje_consistencia >= 40:
        mensaje_consistencia = "consistencia buena"
        emoji_consistencia = "👍"
    else:
        mensaje_consistencia = "compromiso inicial"
        emoji_consistencia = "💪"
    
    # Evaluación de promedio de pasos
    if promedio_pasos >= 10000:
        estado_pasos = "¡Excelente! Superas el objetivo de la OMS"
        color_pasos = COLORS['success']
    elif promedio_pasos >= 7500:
        estado_pasos = "Muy bien, estás cerca del objetivo"
        color_pasos = COLORS['warning']
    elif promedio_pasos >= 5000:
        estado_pasos = "Buen inicio, hay espacio para mejorar"
        color_pasos = COLORS['primary']
    else:
        estado_pasos = "Considera aumentar tu actividad diaria"
        color_pasos = COLORS['secondary']
    
    return html.Div([
        # Resumen Ejecutivo
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("📊 Resumen Ejecutivo", 
                           style={'color': COLORS['primary'], 'margin-bottom': '20px'}),
                    html.P([
                        f"Has registrado {años_registro:.1f} años de actividad física ",
                        f"({total_dias:,} días) con una ",
                        html.Strong(f"{mensaje_consistencia} del {porcentaje_consistencia:.1f}% {emoji_consistencia}", 
                                   style={'color': COLORS['success']}),
                        " de días activos. ",
                        f"Tu promedio diario es de {promedio_pasos:,.0f} pasos. ",
                        html.Strong(estado_pasos, style={'color': color_pasos})
                    ], style={'color': COLORS['text'], 'font-size': '16px', 'line-height': '1.8'}),
                    html.Hr(style={'border-color': 'rgba(0, 212, 255, 0.3)', 'margin': '20px 0'}),
                    html.Ul([
                        html.Li([html.Strong(f"{total_pasos:,} pasos totales", 
                                           style={'color': COLORS['primary']})]),
                        html.Li([html.Strong(f"{total_distancia:,.1f} km recorridos", 
                                           style={'color': COLORS['success']}), 
                                f" ({total_distancia/40075*100:.2f}% de la vuelta al mundo)"]),
                        html.Li([html.Strong(f"{total_calorias:,} kcal quemadas", 
                                           style={'color': COLORS['secondary']})]),
                        html.Li([html.Strong(f"{horas_activas:,} horas de actividad", 
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
                        html.P(f"Tu tasa de actividad del {porcentaje_consistencia:.1f}% es {mensaje_consistencia.split()[1]}. ¡Sigue así!" if porcentaje_consistencia >= 60 else f"Intenta aumentar tu consistencia del {porcentaje_consistencia:.1f}% realizando actividad física más días a la semana."),
                    ], style={'margin-bottom': '25px'}),
                    
                    html.Div([
                        html.H5("2. Objetivo OMS (10,000 pasos/día)", 
                               style={'color': COLORS['primary']}),
                        html.P([
                            f"Promedio actual: ",
                            html.Strong(f"{promedio_pasos:,.0f} pasos/día", style={'color': color_pasos})
                        ]),
                        html.P("💡 " + (
                            "¡Felicidades! Ya cumples el objetivo de la OMS" if promedio_pasos >= 10000 
                            else f"Te faltan aproximadamente {10000-promedio_pasos:,.0f} pasos diarios. Intenta agregar caminatas cortas durante el día"
                        ), style={'font-style': 'italic', 'color': COLORS['text_secondary']}),
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
                        html.Strong("trayectoria " + ("excepcional" if porcentaje_consistencia >= 80 else "notable" if porcentaje_consistencia >= 60 else "positiva"), 
                                  style={'color': COLORS['success']}),
                        " con ",
                        html.Strong(f"{total_pasos:,} pasos totales", 
                                  style={'color': COLORS['primary']}),
                        " registrados en ",
                        html.Strong(f"{años_registro:.1f} años", style={'color': COLORS['warning']}),
                        " y una ",
                        html.Strong(f"consistencia del {porcentaje_consistencia:.1f}%", 
                                  style={'color': COLORS['warning']}),
                        ". ",
                        f"Tu promedio de {promedio_pasos:,.0f} pasos/día demuestra tu compromiso. ",
                        "¡Continúa con tu rutina" + (" y considera agregar más variedad para un fitness completo!" if promedio_pasos >= 7500 else " e intenta aumentar gradualmente tu actividad diaria!")
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
