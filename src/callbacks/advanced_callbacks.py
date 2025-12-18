"""
Callbacks del dashboard avanzado
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
from src.visualizations.advanced_charts import (
    create_heatmap_calendar, create_weight_trend_chart, create_speed_analysis_chart,
    create_heart_rate_chart, create_year_comparison_chart, create_goals_progress_chart,
    create_intensity_chart, create_predictive_chart
)


def register_advanced_callbacks(app, df):
    """Registra todos los callbacks del dashboard avanzado"""
    
    @callback(
        Output('adv-total-steps', 'children'),
        Output('adv-avg-steps', 'children'),
        Output('adv-total-distance', 'children'),
        Output('adv-distance-world', 'children'),
        Output('adv-total-calories', 'children'),
        Output('adv-avg-calories', 'children'),
        Output('adv-total-active-minutes', 'children'),
        Output('adv-active-hours', 'children'),
        Output('heatmap-calendar', 'figure'),
        Output('weight-trend', 'figure'),
        Output('speed-analysis', 'figure'),
        Output('heart-rate-analysis', 'figure'),
        Output('year-comparison', 'figure'),
        Output('goals-progress', 'figure'),
        Output('top-rankings', 'children'),
        Output('intensity-analysis', 'figure'),
        Output('predictive-analysis', 'figure'),
        Input('adv-date-range', 'start_date'),
        Input('adv-date-range', 'end_date')
    )
    def update_advanced_dashboard(start_date, end_date):
        # Filtrar datos
        filtered_df = filter_data_by_date(df, start_date, end_date)
        
        # Calcular métricas para tarjetas
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
        
        # Crear visualizaciones
        heatmap_fig = create_heatmap_calendar(filtered_df)
        weight_fig = create_weight_trend_chart(filtered_df)
        speed_fig = create_speed_analysis_chart(filtered_df)
        hr_fig = create_heart_rate_chart(filtered_df)
        year_fig = create_year_comparison_chart(df)  # Usar df completo para comparar años
        goals_fig = create_goals_progress_chart(filtered_df)
        intensity_fig = create_intensity_chart(filtered_df)
        predictive_fig = create_predictive_chart(filtered_df)
        
        # Crear tabla de rankings
        rankings_table = create_top_rankings_table(filtered_df)
        
        return (card_total_steps, card_avg_steps, card_total_distance, card_distance_world,
                card_total_calories, card_avg_calories, card_total_active_minutes, card_active_hours,
                heatmap_fig, weight_fig, speed_fig, hr_fig, year_fig, goals_fig,
                rankings_table, intensity_fig, predictive_fig)


def create_top_rankings_table(df):
    """Crea tabla con top 10 mejores días"""
    top_pasos = df.nlargest(10, 'Recuento de pasos')[['Fecha', 'Recuento de pasos', 'Distancia_km']].copy()
    top_pasos['Ranking'] = range(1, len(top_pasos) + 1)
    
    return html.Div([
        html.Table([
            html.Thead(html.Tr([
                html.Th('🏆', style={'color': COLORS['warning'], 'text-align': 'center', 'padding': '10px'}),
                html.Th('Fecha', style={'color': COLORS['primary'], 'padding': '10px'}),
                html.Th('Pasos', style={'color': COLORS['primary'], 'padding': '10px'}),
                html.Th('Distancia', style={'color': COLORS['primary'], 'padding': '10px'})
            ])),
            html.Tbody([
                html.Tr([
                    html.Td(f"{row['Ranking']}", style={
                        'text-align': 'center',
                        'padding': '8px',
                        'color': COLORS['warning'] if row['Ranking'] <= 3 else COLORS['text']
                    }),
                    html.Td(row['Fecha'].strftime('%d/%m/%Y'), style={'padding': '8px', 'color': COLORS['text']}),
                    html.Td(f"{int(row['Recuento de pasos']):,}", style={
                        'padding': '8px',
                        'color': COLORS['success'],
                        'font-weight': 'bold'
                    }),
                    html.Td(f"{row['Distancia_km']:.2f} km", style={'padding': '8px', 'color': COLORS['text']})
                ]) for _, row in top_pasos.iterrows()
            ])
        ], style={'width': '100%', 'border-collapse': 'collapse'})
    ])
