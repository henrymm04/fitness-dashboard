"""
Funciones para crear visualizaciones avanzadas
"""
import plotly.graph_objects as go
import numpy as np
from datetime import timedelta
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config.settings import COLORS, CHART_CONFIG, GOALS


def create_heatmap_calendar(df):
    """Crea calendario heatmap de actividad"""
    heatmap_data = df[df['Recuento de pasos'] > 0].copy()
    heatmap_data['DíaSemana'] = heatmap_data['Fecha'].dt.dayofweek
    heatmap_data['Semana'] = heatmap_data['Fecha'].dt.isocalendar().week
    heatmap_data['Año'] = heatmap_data['Fecha'].dt.year
    
    pivot_data = heatmap_data.pivot_table(
        values='Recuento de pasos',
        index='Semana',
        columns='DíaSemana',
        aggfunc='sum',
        fill_value=0
    )
    
    for day in range(7):
        if day not in pivot_data.columns:
            pivot_data[day] = 0
    
    pivot_data = pivot_data.sort_index(axis=1)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
        y=[f'Semana {int(i)}' for i in pivot_data.index],
        colorscale=[[0, COLORS['surface']], [0.5, COLORS['warning']], [1, COLORS['success']]],
        showscale=True,
        hovertemplate='%{x}<br>Semana %{y}<br>Pasos: %{z:,.0f}<extra></extra>',
        colorbar=dict(title='Pasos')
    ))
    
    fig.update_layout(
        **CHART_CONFIG,
        xaxis=dict(side='top'),
        height=400
    )
    
    return fig


def create_weight_trend_chart(df):
    """Crea gráfico de evolución de peso"""
    weight_data = df[df['Peso medio (kg)'] > 0].copy()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=weight_data['Fecha'],
        y=weight_data['Peso medio (kg)'],
        mode='lines+markers',
        name='Peso',
        line=dict(color=COLORS['secondary'], width=3),
        marker=dict(size=6),
        fill='tozeroy',
        fillcolor='rgba(255, 107, 157, 0.1)'
    ))
    
    fig.update_layout(
        **CHART_CONFIG,
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', title='Peso (kg)'),
        hovermode='x unified'
    )
    
    return fig


def create_speed_analysis_chart(df):
    """Crea gráfico de análisis de velocidad y pace"""
    speed_data = df[df['Velocidad_kmh'] > 0].copy()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=speed_data['Fecha'],
        y=speed_data['Velocidad_kmh'],
        mode='lines',
        name='Velocidad (km/h)',
        line=dict(color=COLORS['primary'], width=2)
    ))
    fig.add_trace(go.Scatter(
        x=speed_data['Fecha'],
        y=speed_data['Pace_min_km'],
        mode='lines',
        name='Pace (min/km)',
        line=dict(color=COLORS['warning'], width=2),
        yaxis='y2'
    ))
    
    fig.update_layout(
        **CHART_CONFIG,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(title='Velocidad (km/h)', gridcolor='rgba(255,255,255,0.05)'),
        yaxis2=dict(title='Pace (min/km)', overlaying='y', side='right', gridcolor='rgba(255,255,255,0.05)')
    )
    
    return fig


def create_heart_rate_chart(df):
    """Crea gráfico de frecuencia cardíaca"""
    hr_data = df[df['Frecuencia cardiaca media (ppm)'] > 0].copy()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hr_data['Fecha'],
        y=hr_data['Frecuencia cardiaca máxima (ppm)'],
        mode='lines',
        name='FC Máxima',
        line=dict(color=COLORS['secondary'], width=1),
        fill=None
    ))
    fig.add_trace(go.Scatter(
        x=hr_data['Fecha'],
        y=hr_data['Frecuencia cardiaca media (ppm)'],
        mode='lines',
        name='FC Media',
        line=dict(color=COLORS['primary'], width=2)
    ))
    fig.add_trace(go.Scatter(
        x=hr_data['Fecha'],
        y=hr_data['Frecuencia cardíaca mínima (ppm)'],
        mode='lines',
        name='FC Mínima',
        line=dict(color=COLORS['success'], width=1),
        fill='tonexty',
        fillcolor='rgba(0, 212, 255, 0.1)'
    ))
    
    fig.update_layout(
        **CHART_CONFIG,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(title='BPM', gridcolor='rgba(255,255,255,0.05)'),
        hovermode='x unified'
    )
    
    return fig


def create_year_comparison_chart(df):
    """Crea comparativa año vs año"""
    yearly_comparison = df.groupby('Año').agg({
        'Recuento de pasos': 'sum',
        'Distancia_km': 'sum',
        'Calorías (kcal)': 'sum'
    }).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=yearly_comparison['Año'],
        y=yearly_comparison['Recuento de pasos'],
        name='Pasos',
        marker_color=COLORS['primary'],
        text=yearly_comparison['Recuento de pasos'].apply(lambda x: f'{int(x/1000)}K'),
        textposition='outside'
    ))
    
    fig.update_layout(
        **CHART_CONFIG,
        showlegend=False,
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', type='category'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', title='Pasos Totales')
    )
    
    return fig


def create_goals_progress_chart(df):
    """Crea gráfico de progreso hacia objetivos"""
    dias_con_datos = len(df[df['Recuento de pasos'] > 0])
    dias_objetivo_pasos = len(df[df['Recuento de pasos'] >= GOALS['daily_steps']])
    dias_objetivo_distancia = len(df[df['Distancia_km'] >= GOALS['daily_distance']])
    dias_objetivo_calorias = len(df[df['Calorías (kcal)'] >= GOALS['daily_calories']])
    
    porcentaje_pasos = (dias_objetivo_pasos / dias_con_datos * 100) if dias_con_datos > 0 else 0
    porcentaje_distancia = (dias_objetivo_distancia / dias_con_datos * 100) if dias_con_datos > 0 else 0
    porcentaje_calorias = (dias_objetivo_calorias / dias_con_datos * 100) if dias_con_datos > 0 else 0
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[porcentaje_pasos, porcentaje_distancia, porcentaje_calorias],
        y=[f'{GOALS["daily_steps"]:,} Pasos/día', f'{GOALS["daily_distance"]} km/día', f'{GOALS["daily_calories"]:,} kcal/día'],
        orientation='h',
        marker=dict(color=[COLORS['primary'], COLORS['success'], COLORS['secondary']]),
        text=[f'{porcentaje_pasos:.1f}%', f'{porcentaje_distancia:.1f}%', f'{porcentaje_calorias:.1f}%'],
        textposition='outside'
    ))
    
    fig.update_layout(
        **CHART_CONFIG,
        showlegend=False,
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)', title='% de días alcanzando objetivo', range=[0, 100]),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)')
    )
    
    return fig


def create_intensity_chart(df):
    """Crea gráfico de intensidad de entrenamiento"""
    intensity_data = df[df['Minutos de cardio'] > 0].copy()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=intensity_data['Fecha'],
        y=intensity_data['Puntos Cardio'],
        mode='lines+markers',
        name='Puntos Cardio',
        line=dict(color=COLORS['secondary'], width=2),
        fill='tozeroy',
        fillcolor='rgba(255, 107, 157, 0.2)'
    ))
    
    fig.update_layout(
        **CHART_CONFIG,
        showlegend=False,
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', title='Puntos Cardio')
    )
    
    return fig


def create_predictive_chart(df):
    """Crea gráfico de análisis predictivo"""
    recent_data = df.tail(30)
    
    if len(recent_data) > 1:
        z = np.polyfit(range(len(recent_data)), recent_data['Recuento de pasos'], 1)
        p = np.poly1d(z)
        
        future_days = 30
        import pandas as pd
        future_dates = pd.date_range(df['Fecha'].max() + timedelta(days=1), periods=future_days)
        future_steps = [p(len(recent_data) + i) for i in range(future_days)]
    else:
        future_dates = []
        future_steps = []
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Fecha'],
        y=df['Recuento de pasos'],
        mode='lines',
        name='Datos Reales',
        line=dict(color=COLORS['primary'], width=2)
    ))
    
    if len(future_dates) > 0:
        fig.add_trace(go.Scatter(
            x=future_dates,
            y=future_steps,
            mode='lines',
            name='Proyección',
            line=dict(color=COLORS['warning'], width=2, dash='dash')
        ))
    
    fig.update_layout(
        **CHART_CONFIG,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', title='Pasos'),
        hovermode='x unified'
    )
    
    return fig
