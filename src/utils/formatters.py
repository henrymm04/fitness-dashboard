"""
Utilidades para formatear datos y textos
"""


def format_number(num):
    """Formatea un número con separadores de miles"""
    return f"{int(num):,}"


def format_distance(km):
    """Formatea distancia en kilómetros"""
    return f"{km:,.1f} km"


def format_percentage(value):
    """Formatea un valor como porcentaje"""
    return f"{value:.1f}%"


def format_calories(cal):
    """Formatea calorías"""
    return f"{int(cal):,} kcal"


def format_time_minutes(minutes):
    """Convierte minutos a formato legible"""
    hours = int(minutes / 60)
    return f"{hours:,} horas"


def format_world_laps(km):
    """Calcula porcentaje de vuelta al mundo (40,075 km)"""
    return f"≈ {km/40075*100:.1f}% vuelta al mundo"
