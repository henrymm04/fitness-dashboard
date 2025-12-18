# 🚀 Guía de Inicio Rápido - Fitness Dashboard

## ⚡ Inicio Rápido (3 pasos)

### 1. Configurar Ruta de Datos
Edita `config/settings.py` línea 7:
```python
DATA_PATH = r'C:\TU_RUTA\Métricas de actividad diaria.csv'
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Iniciar Dashboard

#### Opción A: Script de inicio (Windows)
Doble clic en: `start_all.bat`

#### Opción B: Desde terminal
```bash
python app.py
```

## 📱 Acceso al Dashboard

- **URL**: http://127.0.0.1:8050/
- **Navegación por Pestañas**:
  - 🏠 **Dashboard Principal**: Vista general de métricas, gráficos de tendencias, tabla jerárquica
  - 🚀 **Análisis Avanzado**: Heatmap de actividad, análisis de peso y velocidad, predicciones y rankings
  - 🎯 **Conclusiones**: Análisis detallado, recomendaciones e insights clave

## 🎯 Personalización Rápida

### Cambiar Colores
`config/settings.py` - Sección `COLORS`:
```python
COLORS = {
    'primary': '#00d4ff',     # Azul cian
    'secondary': '#ff6b9d',   # Rosa
    'success': '#00ff88',     # Verde
    'warning': '#ffd93d',     # Amarillo
}
```

### Cambiar Objetivos
`config/settings.py` - Sección `GOALS`:
```python
GOALS = {
    'daily_steps': 10000,     # Meta de pasos diarios
    'daily_distance': 5,      # Meta de km diarios
    'daily_calories': 2000    # Meta de calorías
}
```

### Cambiar Puertos
`config/settings.py` - Sección `PORTS`:
```python
PORTS = {
    'main': 8050,
    'conclusions': 8051,
    'advanced': 8052
}
```

## 🛠️ Estructura del Proyecto

```
fitness_dashboard/
├── app_main.py              ⭐ INICIO - Dashboard Principal
├── app_advanced.py          ⭐ INICIO - Dashboard Avanzado
├── conclusiones.py          ⭐ INICIO - Conclusiones
├── start_all.bat            🚀 Lanzar todo (Windows)
│
├── config/
│   └── settings.py          ⚙️ CONFIGURACIÓN AQUÍ
│
├── src/
│   ├── components/          🧩 Componentes UI
│   ├── layouts/             📐 Layouts de páginas
│   ├── callbacks/           🔗 Lógica de interactividad
│   ├── visualizations/      📊 Gráficos
│   └── utils/               🛠️ Utilidades
│
└── data/                    📁 (Opcional) Datos locales
```

## 📊 Datos Requeridos

Tu CSV de Google Fit debe tener estas columnas (mínimo):
- ✅ `Fecha`
- ✅ `Recuento de pasos`
- ✅ `Distancia (m)`
- ✅ `Calorías (kcal)`
- ✅ `Recuento de Minutos Activos`

Columnas opcionales para análisis avanzado:
- 🔸 `Velocidad media (m/s)`
- 🔸 `Frecuencia cardiaca media (ppm)`
- 🔸 `Peso medio (kg)`

## 🎨 Features Principales

### Dashboard Principal
- 📈 Evolución de pasos con promedio
- 🥧 Distribución de actividad
- 📅 Métricas mensuales
- 🗓️ Actividad por día de semana
- 📋 Tabla año → mes → totales

### Dashboard Avanzado
- 🌡️ Heatmap estilo GitHub
- ⚖️ Tendencia de peso
- 🏃 Análisis velocidad/pace
- ❤️ Zonas de frecuencia cardíaca
- 📊 Comparativa año vs año
- 🎯 Progreso objetivos
- 🏆 Top 10 mejores días
- 💪 Intensidad cardio
- 🔮 Proyección 30 días

## 🔧 Solución de Problemas

### Error: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Error: "FileNotFoundError" (CSV no encontrado)
1. Verifica `config/settings.py`
2. Asegúrate que la ruta es correcta
3. Usa `r'C:\ruta\...'` (raw string)

### Gráficos no se actualizan
1. Verifica que el filtro de fechas tenga datos
2. Recarga la página (F5)
3. Revisa la consola por errores

### Puerto ya en uso
1. Cambia puertos en `config/settings.py`
2. O cierra otras instancias de las apps

## 💡 Tips

### 1. Filtro de Fechas
- El filtro actualiza **todas** las visualizaciones
- Incluye tarjetas de métricas
- Prueba diferentes rangos para insights

### 2. Navegación
- Usa botones de navegación entre páginas
- Se abren en nueva pestaña

### 3. Interactividad
- Hover sobre gráficos para detalles
- Zoom y pan habilitados
- Doble click para reset

### 4. Exportar Gráficos
- Hover en gráfico → Botón de cámara
- Descarga como PNG

## 📚 Documentación Completa

- **README.md**: Descripción completa del proyecto
- **ARCHITECTURE.md**: Arquitectura y patrones de diseño
- **QUICKSTART.md**: Esta guía (tú estás aquí)

## 🆘 Ayuda

### Errores Comunes

**"Import config.settings could not be resolved"**
- ✅ Ignora este warning de Pylance
- El código funciona correctamente
- Se arregla con PYTHONPATH en producción

**Gráficos vacíos**
- Verifica que tu CSV tenga datos en el rango seleccionado
- Revisa columnas requeridas

**Encoding errors**
- El código maneja automáticamente UTF-8 y Latin-1
- Si persiste, abre CSV y guarda como UTF-8

## 🎉 ¡Listo para Usar!

1. ✅ Configurar `DATA_PATH`
2. ✅ `pip install -r requirements.txt`
3. ✅ `python app_main.py`
4. ✅ Abrir http://127.0.0.1:8050/

**¡Disfruta analizando tus datos de fitness!** 🏃‍♂️💪📊

---

**Próximos pasos sugeridos**:
- Explora diferentes rangos de fechas
- Compara tus años de actividad
- Identifica patrones en el heatmap
- Revisa tus mejores días en el Top 10
- Analiza la proyección predictiva
