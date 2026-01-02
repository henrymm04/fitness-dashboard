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
    
    # Mapear columnas en inglés a español para compatibilidad con el resto del código
    column_mapping = {
        'Date': 'Fecha',
        'Step count': 'Recuento de pasos',
        'Distance (m)': 'Distancia (m)',
        'Calories (kcal)': 'Calorías (kcal)',
        'Move Minutes count': 'Recuento de Minutos Activos',
        'Active minutes count': 'Recuento de Minutos Activos',
        'Heart Minutes': 'Recuento de Minutos Activos',
        'Heart Points': 'Puntos Cardio',
        'Cardio minutes': 'Minutos de cardio',
        'Average speed (m/s)': 'Velocidad media (m/s)',
        'Max speed (m/s)': 'Velocidad máxima (m/s)',
        'Average weight (kg)': 'Peso medio (kg)',
        'Max weight (kg)': 'Peso máximo (kg)',
        'Min weight (kg)': 'Peso mínimo (kg)',
        'Average heart rate (bpm)': 'Frecuencia cardiaca media (ppm)',
        'Max heart rate (bpm)': 'Frecuencia cardiaca máxima (ppm)',
        'Min heart rate (bpm)': 'Frecuencia cardiaca mínima (ppm)'
    }
    
    # Renombrar columnas que existan
    df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns}, inplace=True)
    
    # Eliminar columnas duplicadas (mantener solo la primera ocurrencia)
    df = df.loc[:, ~df.columns.duplicated()]
    
    # Crear columnas faltantes con valores por defecto si no existen
    required_columns = {
        'Recuento de Minutos Activos': 0,
        'Velocidad media (m/s)': 0,
        'Velocidad máxima (m/s)': 0,
        'Peso medio (kg)': 0,
        'Peso promedio (kg)': 0,
        'Peso máximo (kg)': 0,
        'Peso mínimo (kg)': 0,
        'Frecuencia cardiaca media (ppm)': 0,
        'Frecuencia cardiaca máxima (ppm)': 0,
        'Frecuencia cardiaca mínima (ppm)': 0,
        'Minutos de cardio': 0,
        'Puntos Cardio': 0
    }
    for col, default_value in required_columns.items():
        if col not in df.columns:
            df[col] = default_value
    
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
