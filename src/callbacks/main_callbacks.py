"""
Callbacks del dashboard principal
"""
from dash import Output, Input, callback, html
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config.settings import COLORS
from src.utils.data_loader import filter_data_by_date
from src.utils.formatters import (
    format_number, format_distance, format_calories,
    format_time_minutes, format_world_laps
)
from src.visualizations.basic_charts import (
    create_steps_trend_chart, create_activity_pie_chart,
    create_monthly_metrics_chart, create_weekday_chart
)


def register_main_callbacks(app, df):
    """Registra todos los callbacks del dashboard principal"""
    
    @callback(
        Output('total-steps', 'children'),
        Output('avg-steps', 'children'),
        Output('total-distance', 'children'),
        Output('distance-world', 'children'),
        Output('total-calories', 'children'),
        Output('avg-calories', 'children'),
        Output('total-active-minutes', 'children'),
        Output('active-hours', 'children'),
        Output('steps-trend', 'figure'),
        Output('activity-distribution', 'figure'),
        Output('monthly-metrics', 'figure'),
        Output('weekday-activity', 'figure'),
        Output('hierarchical-table', 'children'),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date')
    )
    def update_dashboard(start_date, end_date):
        # Filtrar datos
        filtered_df = filter_data_by_date(df, start_date, end_date)
        
        # Calcular métricas
        filtered_total_steps = filtered_df['Recuento de pasos'].sum()
        filtered_total_distance = filtered_df['Distancia_km'].sum()
        filtered_total_calories = filtered_df['Calorías (kcal)'].sum()
        filtered_total_active_minutes = filtered_df['Recuento de Minutos Activos'].sum()
        filtered_days = len(filtered_df[filtered_df['Recuento de pasos'] > 0])
        filtered_avg_steps = filtered_df[filtered_df['Recuento de pasos'] > 0]['Recuento de pasos'].mean() if filtered_days > 0 else 0
        
        # Formatear valores de tarjetas
        card_total_steps = format_number(filtered_total_steps)
        card_avg_steps = f"~{format_number(filtered_avg_steps)} pasos/día" if filtered_days > 0 else "Sin datos"
        card_total_distance = format_distance(filtered_total_distance)
        card_distance_world = format_world_laps(filtered_total_distance)
        card_total_calories = format_number(filtered_total_calories)
        card_avg_calories = f"~{format_number(filtered_total_calories/filtered_days)} kcal/día" if filtered_days > 0 else "Sin datos"
        card_total_active_minutes = format_number(filtered_total_active_minutes)
        card_active_hours = format_time_minutes(filtered_total_active_minutes)
        
        # Crear gráficos
        steps_fig = create_steps_trend_chart(filtered_df)
        activity_fig = create_activity_pie_chart(filtered_df)
        monthly_fig = create_monthly_metrics_chart(filtered_df)
        weekday_fig = create_weekday_chart(filtered_df)
        
        # Crear tabla jerárquica
        hierarchical_table = create_hierarchical_table(filtered_df)
        
        return (card_total_steps, card_avg_steps, card_total_distance, card_distance_world,
                card_total_calories, card_avg_calories, card_total_active_minutes, card_active_hours,
                steps_fig, activity_fig, monthly_fig, weekday_fig, hierarchical_table)


def create_hierarchical_table(df):
    """Crea tabla jerárquica año → mes → totales"""
    import pandas as pd
    
    yearly_data = df.groupby('Año').agg({
        'Recuento de pasos': 'sum',
        'Distancia_km': 'sum',
        'Calorías (kcal)': 'sum'
    }).reset_index().sort_values('Año', ascending=False)
    
    rows = []
    for _, year_row in yearly_data.iterrows():
        year = year_row['Año']
        rows.append(html.Tr([
            html.Td(f"📅 {int(year)}", style={
                'padding': '15px',
                'color': COLORS['primary'],
                'font-weight': 'bold',
                'font-size': '18px',
                'border-bottom': f'2px solid {COLORS["primary"]}'
            }),
            html.Td(f"{int(year_row['Recuento de pasos']):,}", style={
                'padding': '15px',
                'color': COLORS['text'],
                'font-weight': 'bold',
                'border-bottom': f'2px solid {COLORS["primary"]}'
            }),
            html.Td(f"{year_row['Distancia_km']:,.1f} km", style={
                'padding': '15px',
                'color': COLORS['text'],
                'font-weight': 'bold',
                'border-bottom': f'2px solid {COLORS["primary"]}'
            }),
            html.Td(f"{int(year_row['Calorías (kcal)']):,} kcal", style={
                'padding': '15px',
                'color': COLORS['text'],
                'font-weight': 'bold',
                'border-bottom': f'2px solid {COLORS["primary"]}'
            })
        ]))
        
        monthly_data = df[df['Año'] == year].groupby(['Mes', 'MesNombre']).agg({
            'Recuento de pasos': 'sum',
            'Distancia_km': 'sum',
            'Calorías (kcal)': 'sum'
        }).reset_index().sort_values('Mes', ascending=False)
        
        for _, month_row in monthly_data.iterrows():
            rows.append(html.Tr([
                html.Td(f"  ↳ {month_row['MesNombre']}", style={
                    'padding': '10px 15px 10px 40px',
                    'color': COLORS['text_secondary'],
                    'font-size': '14px'
                }),
                html.Td(f"{int(month_row['Recuento de pasos']):,}", style={
                    'padding': '10px 15px',
                    'color': COLORS['text_secondary'],
                    'font-size': '14px'
                }),
                html.Td(f"{month_row['Distancia_km']:,.1f} km", style={
                    'padding': '10px 15px',
                    'color': COLORS['text_secondary'],
                    'font-size': '14px'
                }),
                html.Td(f"{int(month_row['Calorías (kcal)']):,} kcal", style={
                    'padding': '10px 15px',
                    'color': COLORS['text_secondary'],
                    'font-size': '14px'
                })
            ]))
    
    return html.Table([
        html.Thead(html.Tr([
            html.Th('Período', style={'color': COLORS['primary'], 'padding': '15px', 'text-align': 'left'}),
            html.Th('Pasos', style={'color': COLORS['primary'], 'padding': '15px', 'text-align': 'left'}),
            html.Th('Distancia', style={'color': COLORS['primary'], 'padding': '15px', 'text-align': 'left'}),
            html.Th('Calorías', style={'color': COLORS['primary'], 'padding': '15px', 'text-align': 'left'})
        ])),
        html.Tbody(rows)
    ], style={'width': '100%', 'border-collapse': 'collapse'})
