"""
Utilidades para formatear datos y textos
"""
import pandas as pd


def format_number(num):
    """Formatea un número con separadores de miles"""
    # Manejar Series de pandas
    if isinstance(num, pd.Series):
        num = num.iloc[0] if len(num) > 0 else 0
    # Manejar valores None o NaN
    if pd.isna(num):
        return "0"
    return f"{int(num):,}"


def format_distance(km):
    """Formatea distancia en kilómetros"""
    # Manejar Series de pandas
    if isinstance(km, pd.Series):
        km = km.iloc[0] if len(km) > 0 else 0
    # Manejar valores None o NaN
    if pd.isna(km):
        return "0.0 km"
    return f"{km:,.1f} km"


def format_percentage(value):
    """Formatea un valor como porcentaje"""
    # Manejar Series de pandas
    if isinstance(value, pd.Series):
        value = value.iloc[0] if len(value) > 0 else 0
    # Manejar valores None o NaN
    if pd.isna(value):
        return "0.0%"
    return f"{value:.1f}%"


def format_calories(cal):
    """Formatea calorías"""
    # Manejar Series de pandas
    if isinstance(cal, pd.Series):
        cal = cal.iloc[0] if len(cal) > 0 else 0
    # Manejar valores None o NaN
    if pd.isna(cal):
        return "0 kcal"
    return f"{int(cal):,} kcal"


def format_time_minutes(minutes):
    """Convierte minutos a formato legible"""
    # Manejar Series de pandas
    if isinstance(minutes, pd.Series):
        minutes = minutes.iloc[0] if len(minutes) > 0 else 0
    # Manejar valores None o NaN
    if pd.isna(minutes):
        return "0 horas"
    hours = int(minutes / 60)
    return f"{hours:,} horas"


def format_world_laps(km):
    """Calcula porcentaje de vuelta al mundo (40,075 km)"""
    return f"≈ {km/40075*100:.1f}% vuelta al mundo"
