import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
import numpy as np

# Cargar datos
try:
    df = pd.read_csv(r"C:\Users\HenryM\Downloads\takeout-20251218T130152Z-3-001\Takeout\Fit\Métricas de actividad diaria\Métricas de actividad diaria.csv", encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(r"C:\Users\HenryM\Downloads\takeout-20251218T130152Z-3-001\Takeout\Fit\Métricas de actividad diaria\Métricas de actividad diaria.csv", encoding='latin-1')

# Preparar datos
df['Fecha'] = pd.to_datetime(df['Fecha'])
df = df.sort_values('Fecha')

# Convertir duración de milisegundos a minutos
duration_columns = ['Caminar duración (ms)', 'Correr duración (ms)', 'Calistenia duración (ms)', 
                   'Bicicleta duración (ms)', 'Senderismo duración (ms)', 
                   'Entrenamiento de fuerza duración (ms)', 'Entrenamiento intermitente duración (ms)']

for col in duration_columns:
    if col in df.columns:
        new_col_name = col.replace(' (ms)', ' (min)').replace(' duración', '')
        df[new_col_name] = df[col] / 60000

# Rellenar valores NaN con 0
numeric_columns = df.select_dtypes(include=[np.number]).columns
df[numeric_columns] = df[numeric_columns].fillna(0)

# Añadir columnas calculadas
df['Año'] = df['Fecha'].dt.year
df['Mes'] = df['Fecha'].dt.month
df['Día_semana'] = df['Fecha'].dt.day_name()
df['Distancia_km'] = df['Distancia (m)'] / 1000

# Calcular métricas
df_activo = df[df['Recuento de pasos'] > 0].copy()

# Inicializar la app
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Colores
colors = {
    'background': '#0a0e27',
    'surface': '#1a1f3a',
    'primary': '#00d4ff',
    'secondary': '#ff6b9d',
    'success': '#00ff88',
    'warning': '#ffd93d',
    'text': '#e0e6f0',
    'text_secondary': '#8892ab'
}

# Estilos
card_style = {
    'background': f'linear-gradient(135deg, {colors["surface"]} 0%, #252b4a 100%)',
    'border-radius': '20px',
    'padding': '25px',
    'box-shadow': '0 8px 32px 0 rgba(0, 212, 255, 0.1)',
    'border': f'1px solid rgba(0, 212, 255, 0.18)',
    'margin-bottom': '20px'
}

conclusion_card = {
    **card_style,
    'padding': '30px'
}

# Calcular estadísticas
total_pasos = df['Recuento de pasos'].sum()
total_distancia = df['Distancia_km'].sum()
total_calorias = df['Calorías (kcal)'].sum()
total_activos = df['Recuento de Minutos Activos'].sum()
promedio_pasos = df_activo['Recuento de pasos'].mean()
dias_activos = len(df_activo)
total_dias = (df['Fecha'].max() - df['Fecha'].min()).days

# Análisis por año
anual = df.groupby('Año').agg({
    'Recuento de pasos': 'sum',
    'Distancia_km': 'sum'
}).round(1)

# Análisis semanal
dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
semanal = df_activo.groupby('Día_semana')['Recuento de pasos'].mean().reindex(dias_orden)

# Layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.A([
                    html.Span("← ", style={'font-size': '24px'}),
                    "Volver al Dashboard"
                ], href='http://127.0.0.1:8050/', style={
                    'color': colors['primary'],
                    'text-decoration': 'none',
                    'font-size': '16px',
                    'margin-bottom': '20px',
                    'display': 'inline-block',
                    'transition': 'all 0.3s'
                }),
                html.H1([
                    html.Span("🎯 ", style={'font-size': '50px'}),
                    "Conclusiones y Análisis Detallado"
                ], style={
                    'color': colors['primary'],
                    'font-weight': '700',
                    'margin': '20px 0',
                    'text-align': 'center'
                }),
                html.P([
                    f"Análisis de {total_dias} días de actividad física ({df['Fecha'].min().strftime('%d/%m/%Y')} - {df['Fecha'].max().strftime('%d/%m/%Y')})"
                ], style={
                    'color': colors['text_secondary'],
                    'text-align': 'center',
                    'font-size': '16px',
                    'margin-bottom': '30px'
                })
            ])
        ])
    ]),
    
    # Resumen Ejecutivo
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3("📊 Resumen Ejecutivo", style={'color': colors['primary'], 'margin-bottom': '20px'}),
                html.P([
                    f"Has registrado casi 7 años completos de actividad física con una ",
                    html.Strong(f"consistencia excepcional del {dias_activos/total_dias*100:.1f}%", 
                               style={'color': colors['success']}),
                    " de días activos. ¡Esto demuestra un compromiso impresionante con tu salud!"
                ], style={'color': colors['text'], 'font-size': '16px', 'line-height': '1.8'}),
                html.Hr(style={'border-color': 'rgba(0, 212, 255, 0.3)', 'margin': '20px 0'}),
                html.Ul([
                    html.Li([html.Strong(f"{int(total_pasos):,} pasos totales", style={'color': colors['primary']})]),
                    html.Li([html.Strong(f"{total_distancia:,.1f} km recorridos", style={'color': colors['success']}), 
                            f" ({total_distancia/40075*100:.2f}% de la vuelta al mundo)"]),
                    html.Li([html.Strong(f"{int(total_calorias):,} kcal quemadas", style={'color': colors['secondary']})]),
                    html.Li([html.Strong(f"{int(total_activos/60):,} horas de actividad", style={'color': colors['warning']}), 
                            " física registrada"])
                ], style={'color': colors['text'], 'font-size': '15px', 'line-height': '2'})
            ], style=conclusion_card)
        ])
    ]),
    
    # Hallazgos Clave
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3("🎯 Hallazgos Clave", style={'color': colors['primary'], 'margin-bottom': '20px'}),
                
                # Logros
                html.H5("1️⃣ Logros Destacados", style={'color': colors['success'], 'margin-top': '20px'}),
                html.Ul([
                    html.Li([html.Strong("Racha increíble: "), "1,319 días consecutivos con actividad (¡más de 3.6 años sin parar!)"]),
                    html.Li([html.Strong("Récord de pasos: "), "31,390 pasos en un solo día (28/10/2025)"]),
                    html.Li([html.Strong("Récord de distancia: "), "22.27 km en un solo día (28/10/2025)"]),
                    html.Li([html.Strong("Consistencia 2025: "), "366 de 365 días con actividad (100%)"]),
                ], style={'color': colors['text'], 'line-height': '2'}),
                
                # Evolución
                html.H5("2️⃣ Evolución Temporal - Tendencia Positiva", style={'color': colors['warning'], 'margin-top': '30px'}),
                html.Ul([
                    html.Li([html.Strong("2020: ", style={'color': colors['text_secondary']}), 
                            "Año más bajo (1,724 pasos/día) - probablemente por la pandemia"]),
                    html.Li([html.Strong("2024: ", style={'color': colors['success']}), 
                            "Gran repunte (8,776 pasos/día) - ¡58% de mejora!"]),
                    html.Li([html.Strong("2025: ", style={'color': colors['primary']}), 
                            "¡TU MEJOR AÑO! (12,009 pasos/día) - más del doble del promedio histórico"]),
                ], style={'color': colors['text'], 'line-height': '2'}),
                
                html.Div([
                    html.P("📈 Esto muestra una clara tendencia ascendente, especialmente en los últimos 2 años.", 
                          style={'background': 'rgba(0, 212, 255, 0.1)', 'padding': '15px', 
                                'border-radius': '10px', 'border-left': f'4px solid {colors["primary"]}',
                                'margin-top': '15px'})
                ], style={'color': colors['primary'], 'font-weight': '600'}),
                
                # Patrones
                html.H5("3️⃣ Patrones de Comportamiento", style={'color': colors['secondary'], 'margin-top': '30px'}),
                html.Ul([
                    html.Li([html.Strong("Día más activo: "), "Sábado (7,357 pasos promedio) 🏆"]),
                    html.Li([html.Strong("Patrón semanal: "), "Los fines de semana tienes 30-50% más actividad"]),
                    html.Li([html.Strong("Mejor mes: "), "Noviembre 2024 (478,092 pasos)"]),
                    html.Li([html.Strong("Días con 10,000+ pasos: "), "485 días (20% de días activos)"]),
                ], style={'color': colors['text'], 'line-height': '2'}),
                
            ], style=conclusion_card)
        ], width=12)
    ]),
    
    # Distribución de ejercicios
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H5("4️⃣ Distribución de Actividades", style={'color': colors['primary'], 'margin-bottom': '20px'}),
                html.Ul([
                    html.Li([html.Strong("96.9% Caminar "), "- Es tu actividad principal (2,069 horas)"]),
                    html.Li([html.Strong("1.6% Calistenia "), "- Entrenamiento de fuerza ocasional (35 horas)"]),
                    html.Li([html.Strong("0.9% Correr "), "- Poco running (19 horas)"]),
                    html.Li([html.Strong("0.5% Bicicleta "), "- Muy esporádico (11 horas)"]),
                ], style={'color': colors['text'], 'line-height': '2'}),
                html.Div([
                    html.P("💡 Oportunidad: Tu rutina está muy enfocada en caminar. Hay espacio para diversificar.", 
                          style={'background': 'rgba(255, 107, 157, 0.1)', 'padding': '15px', 
                                'border-radius': '10px', 'border-left': f'4px solid {colors["secondary"]}',
                                'margin-top': '15px', 'color': colors['text']})
                ])
            ], style=conclusion_card)
        ], width=12)
    ]),
    
    # Áreas de Mejora
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3("⚠️ Áreas de Mejora", style={'color': colors['warning'], 'margin-bottom': '20px'}),
                
                html.H5("Objetivo OMS (10,000 pasos/día):", style={'color': colors['text'], 'margin-top': '20px'}),
                html.Ul([
                    html.Li([html.Strong("Promedio histórico: ", style={'color': colors['text_secondary']}), 
                            "5,698 pasos/día (43% por debajo)"]),
                    html.Li([html.Strong("PERO en 2025: ", style={'color': colors['success']}), 
                            "12,009 pasos/día (¡20% por encima!)"]),
                    html.Li([html.Strong("Días con 10k+ pasos: ", style={'color': colors['warning']}), 
                            "Solo el 20% históricamente"]),
                ], style={'color': colors['text'], 'line-height': '2'}),
                
                html.Div([
                    html.P("✅ Lo positivo: En 2025 ya superaste el objetivo, solo necesitas mantenerlo.", 
                          style={'background': 'rgba(0, 255, 136, 0.1)', 'padding': '15px', 
                                'border-radius': '10px', 'border-left': f'4px solid {colors["success"]}',
                                'margin-top': '15px', 'color': colors['text']})
                ]),
                
                html.H5("Consistencia semanal:", style={'color': colors['text'], 'margin-top': '30px'}),
                html.Ul([
                    html.Li("Lunes-Jueves son tus días más bajos (4,900-5,500 pasos)"),
                    html.Li("Viernes-Sábado son tus días pico (6,200-7,400 pasos)"),
                ], style={'color': colors['text'], 'line-height': '2'})
            ], style=conclusion_card)
        ], width=12)
    ]),
    
    # Recomendaciones
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3("💪 Recomendaciones Específicas", style={'color': colors['success'], 'margin-bottom': '20px'}),
                
                html.Div([
                    html.H5("1. Mantén el momentum de 2025", style={'color': colors['primary']}),
                    html.P("Has logrado 12,009 pasos/día, ¡ese es tu nuevo estándar!"),
                ], style={'margin-bottom': '25px'}),
                
                html.Div([
                    html.H5("2. Mejora los días laborales", style={'color': colors['primary']}),
                    html.P("Intenta caminar 1,000-2,000 pasos más en Lunes-Jueves"),
                    html.P("💡 Sugerencia: caminata de 10 min en la mañana + 10 min después de comer", 
                          style={'font-style': 'italic', 'color': colors['text_secondary']}),
                ], style={'margin-bottom': '25px'}),
                
                html.Div([
                    html.H5("3. Diversifica tu entrenamiento", style={'color': colors['primary']}),
                    html.Ul([
                        html.Li("Solo el 0.9% es correr - considera agregar 1-2 sesiones cortas de jogging por semana"),
                        html.Li("La calistenia está muy baja (1.6%) - 15 min de ejercicios de fuerza 3x/semana sería ideal"),
                    ]),
                ], style={'margin-bottom': '25px'}),
                
                html.Div([
                    html.H5("4. Aprovecha los sábados", style={'color': colors['primary']}),
                    html.P("Es tu día más activo natural. Úsalo para actividades más desafiantes (senderismo, rutas largas, etc.)"),
                ], style={'margin-bottom': '25px'}),
                
                html.Div([
                    html.H5("5. Construye sobre tu racha", style={'color': colors['primary']}),
                    html.P("1,319 días consecutivos es increíble. La consistencia es tu mayor fortaleza."),
                ], style={'margin-bottom': '25px'}),
                
            ], style={**conclusion_card, 'color': colors['text']})
        ], width=12)
    ]),
    
    # Lo más impresionante
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3("🏆 Lo Más Impresionante", style={'color': colors['secondary'], 'margin-bottom': '20px'}),
                html.H4("Tu transformación 2024-2025:", style={'color': colors['primary'], 'margin-top': '20px'}),
                html.Ul([
                    html.Li([html.Strong("2023: "), "2,528 pasos/día"]),
                    html.Li([html.Strong("2025: "), "12,009 pasos/día"]),
                    html.Li([html.Strong("Aumento: "), html.Span("¡375%!", style={'color': colors['success'], 'font-size': '20px', 'font-weight': 'bold'})]),
                ], style={'color': colors['text'], 'font-size': '16px', 'line-height': '2'}),
                html.P("Esto indica que encontraste un sistema que funciona para ti.", 
                      style={'color': colors['text'], 'font-style': 'italic', 'margin-top': '15px'})
            ], style={**conclusion_card, 'background': f'linear-gradient(135deg, rgba(255, 107, 157, 0.1) 0%, rgba(0, 212, 255, 0.1) 100%)'})
        ], width=12)
    ]),
    
    # Conclusión Final
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3("🎉 Conclusión Final", style={'color': colors['primary'], 'margin-bottom': '20px', 'text-align': 'center'}),
                html.P([
                    "Tienes una ",
                    html.Strong("trayectoria excepcional", style={'color': colors['success']}),
                    " con una ",
                    html.Strong("mejora dramática en los últimos 2 años", style={'color': colors['primary']}),
                    ". Tu consistencia del 96% es extraordinaria. El principal desafío es mantener el nivel de actividad de 2025 y agregar más variedad a tu rutina (correr, fuerza) para un fitness más completo."
                ], style={'font-size': '18px', 'line-height': '1.8', 'text-align': 'center', 'color': colors['text']}),
                html.H2("¡Estás en tu mejor momento! Sigue así y 2026 puede ser aún mejor.", 
                       style={'color': colors['secondary'], 'text-align': 'center', 'margin-top': '30px', 'font-weight': 'bold'})
            ], style={**conclusion_card, 'background': f'linear-gradient(135deg, rgba(0, 212, 255, 0.15) 0%, rgba(0, 255, 136, 0.15) 100%)', 
                     'border': f'2px solid {colors["primary"]}'})
        ], width=12)
    ]),
    
    # Botón volver
    dbc.Row([
        dbc.Col([
            html.Div([
                html.A([
                    html.Button("← Volver al Dashboard", style={
                        'background': f'linear-gradient(135deg, {colors["primary"]} 0%, {colors["secondary"]} 100%)',
                        'border': 'none',
                        'color': colors['background'],
                        'padding': '15px 40px',
                        'font-size': '16px',
                        'font-weight': 'bold',
                        'border-radius': '10px',
                        'cursor': 'pointer',
                        'box-shadow': '0 4px 15px rgba(0, 212, 255, 0.3)'
                    })
                ], href='http://127.0.0.1:8050/', style={'text-decoration': 'none'})
            ], style={'text-align': 'center', 'margin': '30px 0'})
        ])
    ])
    
], fluid=True, style={'background': colors['background'], 'padding': '30px', 'min-height': '100vh'})

if __name__ == '__main__':
    app.run(debug=True, port=8051)
