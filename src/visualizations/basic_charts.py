"""
Funciones para crear visualizaciones básicas
"""
import plotly.graph_objects as go
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config.settings import COLORS, CHART_CONFIG


def create_steps_trend_chart(df):
    """Crea gráfico de tendencia de pasos"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['Fecha'],
        y=df['Recuento de pasos'],
        mode='lines',
        name='Pasos diarios',
        line=dict(color=COLORS['primary'], width=2),
        fill='tozeroy',
        fillcolor='rgba(0, 212, 255, 0.1)',
        hovertemplate='<b>%{x|%d/%m/%Y}</b><br>Pasos: %{y:,.0f}<extra></extra>'
    ))
    
    avg_steps = df[df['Recuento de pasos'] > 0]['Recuento de pasos'].mean()
    fig.add_hline(
        y=avg_steps,
        line_dash="dash",
        line_color=COLORS['warning'],
        annotation_text=f"Promedio: {int(avg_steps):,}",
        annotation_position="right"
    )
    
    fig.update_layout(
        **CHART_CONFIG,
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', title='Fecha'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', title='Pasos'),
        hovermode='x unified',
        height=400
    )
    
    return fig


def create_activity_pie_chart(df):
    """Crea gráfico de pastel de distribución de actividad"""
    df_active = df[df['Recuento de pasos'] > 0]
    
    categories = []
    values = []
    colors_list = []
    
    if len(df_active[df_active['Recuento de pasos'] >= 10000]) > 0:
        categories.append('🏆 Excelente (≥10k)')
        values.append(len(df_active[df_active['Recuento de pasos'] >= 10000]))
        colors_list.append(COLORS['success'])
    
    if len(df_active[(df_active['Recuento de pasos'] >= 5000) & (df_active['Recuento de pasos'] < 10000)]) > 0:
        categories.append('😊 Bueno (5k-10k)')
        values.append(len(df_active[(df_active['Recuento de pasos'] >= 5000) & (df_active['Recuento de pasos'] < 10000)]))
        colors_list.append(COLORS['warning'])
    
    if len(df_active[df_active['Recuento de pasos'] < 5000]) > 0:
        categories.append('📉 Bajo (<5k)')
        values.append(len(df_active[df_active['Recuento de pasos'] < 5000]))
        colors_list.append(COLORS['secondary'])
    
    fig = go.Figure(data=[go.Pie(
        labels=categories,
        values=values,
        hole=0.4,
        marker=dict(colors=colors_list),
        textinfo='label+percent',
        textfont=dict(size=14, color=COLORS['text']),
        hovertemplate='<b>%{label}</b><br>Días: %{value}<br>%{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        **CHART_CONFIG,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(color=COLORS['text'])
        ),
        height=400
    )
    
    return fig


def create_monthly_metrics_chart(df):
    """Crea gráfico de métricas mensuales"""
    monthly_data = df.groupby(['Año', 'Mes']).agg({
        'Recuento de pasos': 'sum',
        'Distancia_km': 'sum',
        'Calorías (kcal)': 'sum'
    }).reset_index()
    
    monthly_data['Mes-Año'] = pd.to_datetime(
        monthly_data['Año'].astype(str) + '-' + monthly_data['Mes'].astype(str) + '-01'
    ).dt.strftime('%b %Y')
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=monthly_data['Mes-Año'],
        y=monthly_data['Recuento de pasos'],
        name='Pasos',
        marker_color=COLORS['primary'],
        yaxis='y',
        hovertemplate='<b>%{x}</b><br>Pasos: %{y:,.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=monthly_data['Mes-Año'],
        y=monthly_data['Distancia_km'],
        name='Distancia (km)',
        line=dict(color=COLORS['success'], width=3),
        yaxis='y2',
        hovertemplate='<b>%{x}</b><br>Distancia: %{y:.1f} km<extra></extra>'
    ))
    
    fig.update_layout(
        **CHART_CONFIG,
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', title='Mes'),
        yaxis=dict(
            title='Pasos',
            gridcolor='rgba(255,255,255,0.05)'
        ),
        yaxis2=dict(
            title='Distancia (km)',
            overlaying='y',
            side='right',
            gridcolor='rgba(255,255,255,0.05)'
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode='x unified',
        height=400
    )
    
    return fig


def create_weekday_chart(df):
    """Crea gráfico de actividad por día de la semana"""
    dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dias_es = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    
    weekday_data = df[df['Recuento de pasos'] > 0].groupby('DíaSemana').agg({
        'Recuento de pasos': 'mean'
    }).reindex(dias_orden).reset_index()
    
    weekday_data['DíaSemana_ES'] = dias_es
    
    colors_weekday = [COLORS['success'] if day in ['Saturday', 'Sunday'] 
                     else COLORS['primary'] for day in weekday_data['DíaSemana']]
    
    fig = go.Figure(data=[go.Bar(
        x=weekday_data['DíaSemana_ES'],
        y=weekday_data['Recuento de pasos'],
        marker_color=colors_weekday,
        text=weekday_data['Recuento de pasos'].apply(lambda x: f'{int(x):,}'),
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Promedio: %{y:,.0f} pasos<extra></extra>'
    )])
    
    fig.update_layout(
        **CHART_CONFIG,
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', title='Día de la Semana'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', title='Promedio de Pasos'),
        height=400
    )
    
    return fig
