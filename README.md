# 💪 Dashboard de Fitness - Google Fit Analytics

Dashboard interactivo y moderno para visualizar tus métricas de actividad física de Google Fit.

![Dashboard Preview](https://img.shields.io/badge/Python-3.x-blue.svg)
![Dash](https://img.shields.io/badge/Dash-2.x-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🚀 Inicio Rápido

### 1. Clonar el repositorio
```bash
git clone https://github.com/henrymm04/fitness-dashboard.git
cd fitness-dashboard
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar tus datos
Reemplaza el archivo `data/metricas_actividad_diaria.csv` con tu propio archivo de Google Fit, o modifica la ruta en `config/settings.py`:

```python
DATA_PATH = 'ruta/a/tu/archivo.csv'
```

### 4. Ejecutar el dashboard
```bash
python app.py
```

Abre tu navegador en: **http://localhost:8050**

## 🎨 Características

- **📊 Visualizaciones Modernas**: Gráficos estilizados con Plotly
- **🌙 Tema Oscuro**: Diseño elegante y minimalista
- **📈 Métricas en Tiempo Real**: Filtra por rango de fechas
- **🗂️ Navegación por Pestañas**: Una sola aplicación con 3 secciones
  - 🏠 Dashboard Principal: Métricas básicas y visualizaciones fundamentales
  - 🚀 Análisis Avanzado: Heatmaps, predicciones y análisis profundos
  - 🎯 Conclusiones: Insights y recomendaciones personalizadas
- **🎯 Análisis Completo**:
  - Evolución de pasos diarios con media móvil
  - Distribución de tipos de actividades
  - Calorías y distancia mensuales
  - Actividad por día de la semana
  - Comparación de ejercicios a lo largo del tiempo

## 📦 Obtener tus datos de Google Fit

1. Ve a [Google Takeout](https://takeout.google.com/)
2. Deselecciona todo y selecciona solo **"Fit"**
3. Descarga tus datos
4. Busca el archivo: `Métricas de actividad diaria.csv`
5. Cópialo a la carpeta `data/` del proyecto

## 📋 Datos Incluidos

El dashboard analiza:
- ✅ Pasos totales y promedios
- ✅ Distancia recorrida (km)
- ✅ Calorías quemadas
- ✅ Minutos activos
- ✅ Tipos de ejercicio (caminar, correr, calistenia, bicicleta, etc.)
- ✅ Tendencias temporales
- ✅ Patrones semanales

## 🎯 Estadísticas Principales

El dashboard muestra 4 tarjetas principales:
1. 🚶 **Pasos Totales** - Con promedio diario
2. 🛣️ **Distancia Total** - En kilómetros
3. 🔥 **Calorías Quemadas** - Total y promedio
4. ⏱️ **Minutos Activos** - Convertidos a horas

## 🛠️ Tecnologías

- Python 3.x
- Plotly & Dash
- Pandas
- Bootstrap Components

## 🛠️ Tecnologías

- Python 3.x
- Plotly & Dash
- Pandas
- Bootstrap Components

## 📁 Estructura del Proyecto

```
fitness_dashboard/
├── app.py                    # Aplicación principal unificada
├── config/
│   └── settings.py          # Configuración (colores, puertos, rutas)
├── src/
│   ├── components/          # Componentes UI reutilizables
│   ├── layouts/             # Layouts de las 3 pestañas
│   ├── callbacks/           # Lógica de interactividad
│   ├── visualizations/      # Gráficos Plotly
│   └── utils/               # Utilidades (carga de datos, formateo)
├── data/                    # Archivo CSV de Google Fit
└── requirements.txt         # Dependencias Python
```

## 📄 Documentación Adicional

- [Guía de Inicio Rápido](QUICKSTART.md) - Instrucciones detalladas paso a paso
- [Arquitectura](ARCHITECTURE.md) - Diseño y flujo de datos
- [Estructura](STRUCTURE.md) - Detalles de organización del código

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

---

✨ **Disfruta explorando tus datos de fitness!**

Si te resulta útil, dale una ⭐ al repositorio!