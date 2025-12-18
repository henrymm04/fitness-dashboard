"""
Utilidades para cargar y procesar datos
"""
import pandas as pd
from datetime import datetime, timedelta
from config.settings import DATA_PATH


def load_fitness_data():
    """
    Carga y preprocesa los datos de Google Fit
    
    Returns:
        pd.DataFrame: DataFrame con los datos procesados
    """
    try:
        df = pd.read_csv(DATA_PATH, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(DATA_PATH, encoding='latin-1')
    
    # Convertir fecha
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%Y-%m-%d')
    
    # Calcular métricas derivadas
    df['Distancia_km'] = (df['Distancia (m)'] / 1000).round(2)
    df['Año'] = df['Fecha'].dt.year
    df['Mes'] = df['Fecha'].dt.month
    df['MesNombre'] = df['Fecha'].dt.strftime('%B')
    df['DíaSemana'] = df['Fecha'].dt.day_name()
    df['Velocidad_kmh'] = (df['Velocidad media (m/s)'] * 3.6).round(2)
    df['Velocidad_max_kmh'] = (df['Velocidad máxima (m/s)'] * 3.6).round(2)
    
    # Calcular pace (min/km)
    df['Pace_min_km'] = 0.0
    mask = df['Velocidad_kmh'] > 0
    df.loc[mask, 'Pace_min_km'] = (60 / df.loc[mask, 'Velocidad_kmh']).round(2)
    
    return df


def calculate_summary_stats(df):
    """
    Calcula estadísticas resumidas del dataset
    
    Args:
        df: DataFrame con los datos
        
    Returns:
        dict: Diccionario con estadísticas clave
    """
    return {
        'total_steps': df['Recuento de pasos'].sum(),
        'total_distance': df['Distancia_km'].sum(),
        'total_calories': df['Calorías (kcal)'].sum(),
        'total_active_minutes': df['Recuento de Minutos Activos'].sum(),
        'active_days': len(df[df['Recuento de pasos'] > 0]),
        'avg_steps': df[df['Recuento de pasos'] > 0]['Recuento de pasos'].mean(),
        'first_date': df['Fecha'].min(),
        'last_date': df['Fecha'].max()
    }


def filter_data_by_date(df, start_date, end_date):
    """
    Filtra datos por rango de fechas
    
    Args:
        df: DataFrame con los datos
        start_date: Fecha de inicio
        end_date: Fecha de fin
        
    Returns:
        pd.DataFrame: DataFrame filtrado
    """
    mask = (df['Fecha'] >= start_date) & (df['Fecha'] <= end_date)
    return df[mask]


def get_date_range(df):
    """
    Obtiene el rango de fechas disponible
    
    Args:
        df: DataFrame con los datos
        
    Returns:
        tuple: (fecha_inicio, fecha_fin)
    """
    return df['Fecha'].min(), df['Fecha'].max()
