"""
Callbacks para la pestaña de Conclusiones
"""
from dash import callback, Output, Input
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.utils.data_loader import filter_data_by_date
from src.layouts.conclusions_layout import create_conclusions_content


def register_conclusions_callbacks(app, df):
    """
    Registra los callbacks para la pestaña de conclusiones
    
    Args:
        app: Instancia de la aplicación Dash
        df: DataFrame con todos los datos
    """
    
    # Callback para sincronizar fechas al Store compartido
    @callback(
        Output('shared-date-store', 'data', allow_duplicate=True),
        Input('conclusions-date-range', 'start_date'),
        Input('conclusions-date-range', 'end_date'),
        prevent_initial_call=True
    )
    def sync_conclusions_dates(start_date, end_date):
        """Actualiza el store compartido cuando cambian las fechas en conclusiones"""
        return {'start_date': start_date, 'end_date': end_date}
    
    # Callback para actualizar el DatePickerRange desde el Store
    @callback(
        Output('conclusions-date-range', 'start_date', allow_duplicate=True),
        Output('conclusions-date-range', 'end_date', allow_duplicate=True),
        Input('shared-date-store', 'data'),
        prevent_initial_call=True
    )
    def update_conclusions_date_picker(date_data):
        """Actualiza el DatePickerRange cuando cambia el store compartido"""
        return date_data['start_date'], date_data['end_date']
    
    @callback(
        Output('conclusions-content', 'children'),
        Input('conclusions-date-range', 'start_date'),
        Input('conclusions-date-range', 'end_date'),
        prevent_initial_call=False
    )
    def update_conclusions(start_date, end_date):
        """Actualiza las conclusiones según el rango de fechas"""
        import pandas as pd
        
        # Si no hay fechas, usar todas las fechas disponibles
        if start_date is None or end_date is None:
            return create_conclusions_content(df)
        
        # Convertir fechas a datetime si son strings
        if isinstance(start_date, str):
            start_date = pd.to_datetime(start_date)
        if isinstance(end_date, str):
            end_date = pd.to_datetime(end_date)
        
        # Filtrar datos por fecha
        filtered_df = filter_data_by_date(df, start_date, end_date)
        
        # Generar contenido de conclusiones
        return create_conclusions_content(filtered_df)
