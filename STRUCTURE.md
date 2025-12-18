# 📁 Estructura Completa del Proyecto

```
fitness_dashboard/
│
├── 📄 app.py                         # 🏠 Dashboard Unificado (Puerto 8050)
│                                      # Incluye 3 pestañas: Principal, Avanzado, Conclusiones
├── 🚀 start_all.bat                  # Script inicio Windows
│
├── 📖 README.md                      # Documentación principal
├── 📖 ARCHITECTURE.md                # Arquitectura detallada
├── 📖 QUICKSTART.md                  # Guía inicio rápido
├── 📖 STRUCTURE.md                   # Este archivo
│
├── 📦 requirements.txt               # Dependencias Python
│
├── 📁 config/                        # ⚙️ CONFIGURACIÓN
│   ├── __init__.py
│   └── settings.py                   # 🎨 Colores, puertos, objetivos, paths
│
├── 📁 src/                           # 💻 CÓDIGO FUENTE MODULAR
│   ├── __init__.py
│   │
│   ├── 📁 components/               # 🧩 COMPONENTES REUTILIZABLES
│   │   ├── __init__.py
│   │   ├── cards.py                 # Tarjetas de estadísticas
│   │   └── navigation.py            # Menús y botones navegación
│   │
    ├── 📁 layouts/                  # 📐 LAYOUTS DE PÁGINAS
│   │   ├── __init__.py
│   │   ├── main_layout.py           # Layout dashboard principal
│   │   ├── advanced_layout.py       # Layout dashboard avanzado
│   │   └── conclusions_layout.py    # Layout de conclusiones
│   │
│   ├── 📁 callbacks/                # 🔗 LÓGICA DE INTERACTIVIDAD
│   │   ├── __init__.py
│   │   ├── main_callbacks.py        # Callbacks dashboard principal
│   │   └── advanced_callbacks.py    # Callbacks dashboard avanzado
│   │
│   ├── 📁 visualizations/           # 📊 GRÁFICOS PLOTLY
│   │   ├── __init__.py
│   │   ├── basic_charts.py          # Gráficos básicos (líneas, barras, pastel)
│   │   └── advanced_charts.py       # Gráficos avanzados (heatmap, predicción)
│   │
│   └── 📁 utils/                    # 🛠️ UTILIDADES
│       ├── __init__.py
│       ├── data_loader.py           # Carga y procesamiento de datos
│       └── formatters.py            # Formateo de números y textos
│
└── 📁 data/                          # 📂 DATOS (opcional)
    └── (CSV files aquí)

```

## 🎯 Archivos por Función

### 🚀 Puntos de Entrada (Ejecutables)

| Archivo | Puerto | Descripción |
|---------|--------|-------------|
| `app.py` | 8050 | Dashboard unificado con navegación por pestañas |
| | | - 🏠 Pestaña Principal: métricas core |
| | | - 🚀 Pestaña Avanzado: análisis y predicciones |
| | | - 🎯 Pestaña Conclusiones: insights y recomendaciones |
| `start_all.bat` | - | Script de inicio para Windows |

### ⚙️ Configuración

| Archivo | Propósito |
|---------|-----------|
| `config/settings.py` | **Configuración central**: colores, puertos, rutas, objetivos |

### 🧩 Componentes UI

| Archivo | Exporta |
|---------|---------|
| `src/components/cards.py` | `create_stat_card()`, `create_info_card()` |
| `src/components/navigation.py` | `create_nav_button()`, `create_back_button()` |

### 📐 Layouts

| Archivo | Función Principal |
|---------|-------------------|
| `src/layouts/main_layout.py` | `create_main_layout(first_date, last_date, total_days)` |
| `src/layouts/advanced_layout.py` | `create_advanced_layout(first_date, last_date)` |

### 🔗 Callbacks

| Archivo | Función Principal |
|---------|-------------------|
| `src/callbacks/main_callbacks.py` | `register_main_callbacks(app, df)` |
| `src/callbacks/advanced_callbacks.py` | `register_advanced_callbacks(app, df)` |

### 📊 Visualizaciones

#### basic_charts.py
- `create_steps_trend_chart(df)` - Evolución de pasos
- `create_activity_pie_chart(df)` - Distribución pastel
- `create_monthly_metrics_chart(df)` - Métricas mensuales
- `create_weekday_chart(df)` - Actividad por día semana

#### advanced_charts.py
- `create_heatmap_calendar(df)` - Calendario heatmap
- `create_weight_trend_chart(df)` - Evolución peso
- `create_speed_analysis_chart(df)` - Velocidad/pace
- `create_heart_rate_chart(df)` - Frecuencia cardíaca
- `create_year_comparison_chart(df)` - Comparativa años
- `create_goals_progress_chart(df)` - Progreso objetivos
- `create_intensity_chart(df)` - Intensidad cardio
- `create_predictive_chart(df)` - Análisis predictivo

### 🛠️ Utilidades

#### data_loader.py
- `load_fitness_data()` - Carga CSV con encoding handling
- `filter_data_by_date(df, start, end)` - Filtrado por fechas
- `calculate_summary_stats(df)` - Estadísticas globales
- `get_date_range(df)` - Rango de fechas disponible

#### formatters.py
- `format_number(num)` - Formato con separadores
- `format_distance(km)` - Formato distancia
- `format_calories(cal)` - Formato calorías
- `format_time_minutes(minutes)` - Conversión a horas
- `format_world_laps(km)` - % vuelta al mundo

## 📊 Flujo de Datos

```
┌─────────────────┐
│   CSV File      │
│  (Google Fit)   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ data_loader.py          │
│ - Carga CSV             │
│ - Transforma datos      │
│ - Calcula métricas      │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ app_main.py /           │
│ app_advanced.py         │
│ - Crea instancia Dash   │
│ - Obtiene fecha range   │
└────────┬────────────────┘
         │
         ├──────────────────┬─────────────────┐
         ▼                  ▼                 ▼
┌─────────────┐    ┌─────────────┐   ┌──────────────┐
│  Layout     │    │  Callbacks  │   │ Visualizat.  │
│  (main/adv) │    │  (filters)  │   │  (charts)    │
└─────────────┘    └─────────────┘   └──────────────┘
         │                  │                 │
         └──────────────────┴─────────────────┘
                            ▼
                    ┌──────────────┐
                    │   Browser    │
                    │ (Dashboard)  │
                    └──────────────┘
```

## 🎨 Dependencias entre Módulos

```
app_main.py
    ├── config.settings (COLORS, PORTS)
    ├── src.utils.data_loader (load_fitness_data)
    ├── src.layouts.main_layout (create_main_layout)
    └── src.callbacks.main_callbacks (register_main_callbacks)

main_layout.py
    ├── config.settings (COLORS, CARD_STYLE)
    ├── src.components.cards (create_stat_card)
    └── src.components.navigation (create_navigation_menu)

main_callbacks.py
    ├── config.settings (COLORS)
    ├── src.utils.data_loader (filter_data_by_date)
    ├── src.utils.formatters (format_*)
    └── src.visualizations.basic_charts (create_*_chart)

advanced_charts.py
    ├── config.settings (COLORS, CHART_CONFIG, GOALS)
    └── plotly.graph_objects
```

## 📦 Tamaño Aproximado de Archivos

| Tipo | Archivo | Líneas | Tamaño |
|------|---------|--------|--------|
| App | `app_main.py` | ~130 | ~5 KB |
| App | `app_advanced.py` | ~90 | ~4 KB |
| Config | `settings.py` | ~60 | ~2 KB |
| Layout | `main_layout.py` | ~140 | ~6 KB |
| Layout | `advanced_layout.py` | ~140 | ~6 KB |
| Callbacks | `main_callbacks.py` | ~170 | ~7 KB |
| Callbacks | `advanced_callbacks.py` | ~140 | ~6 KB |
| Viz | `basic_charts.py` | ~180 | ~8 KB |
| Viz | `advanced_charts.py` | ~280 | ~12 KB |
| Utils | `data_loader.py` | ~100 | ~4 KB |
| Utils | `formatters.py` | ~40 | ~1 KB |
| Components | `cards.py` | ~90 | ~4 KB |
| Components | `navigation.py` | ~100 | ~4 KB |

**Total código modular**: ~1,660 líneas (~69 KB)

## 🔄 Comparación: Antes vs Después

### ❌ Antes (Monolítico)
```
app.py                    # 709 líneas - TODO junto
avanzado.py              # 706 líneas - TODO junto
conclusiones.py          # 350 líneas - TODO junto
```
**Total**: 1,765 líneas en 3 archivos gigantes

### ✅ Después (Modular)
```
15 archivos especializados
Promedio: ~110 líneas por archivo
Responsabilidad única por módulo
```
**Total**: ~1,660 líneas en 15 archivos organizados

### 🎯 Mejoras

| Aspecto | Antes | Después |
|---------|-------|---------|
| **Archivos** | 3 monolíticos | 15+ modulares |
| **Líneas/archivo** | ~700 | ~110 |
| **Reutilización** | Código duplicado | Componentes compartidos |
| **Mantenibilidad** | Difícil (todo mezclado) | Fácil (separado) |
| **Testabilidad** | Imposible | Funciones aisladas |
| **Escalabilidad** | Limitada | Alta |
| **Colaboración** | Conflictos | Trabajo paralelo |
| **Configuración** | Hardcoded | Centralizada |

## 🎓 Próximos Pasos

### Para Desarrolladores
1. Revisar `ARCHITECTURE.md` - Entender patrones
2. Leer `QUICKSTART.md` - Configurar entorno
3. Explorar `src/` - Familiarizarse con módulos
4. Modificar `config/settings.py` - Personalizar

### Para Usuarios
1. `QUICKSTART.md` - Iniciar rápido
2. `start_all.bat` - Lanzar dashboards
3. Explorar dashboards - Analizar datos

## 📚 Documentación Disponible

| Archivo | Audiencia | Contenido |
|---------|-----------|-----------|
| `README.md` | Todos | Descripción completa del proyecto |
| `QUICKSTART.md` | Usuarios | Inicio rápido y configuración |
| `ARCHITECTURE.md` | Desarrolladores | Patrones y arquitectura |
| `STRUCTURE.md` | Todos | Este archivo - mapa del proyecto |

---

**Última actualización**: Refactorización completa - Arquitectura modular implementada
