# 🏗️ Arquitectura del Proyecto - Fitness Dashboard

## Principios de Diseño

Este proyecto sigue principios de **arquitectura limpia** y **separación de responsabilidades**:

1. **Modularidad**: Cada funcionalidad en su propio módulo
2. **Reutilización**: Componentes y funciones compartidas
3. **Mantenibilidad**: Código organizado y documentado
4. **Escalabilidad**: Fácil agregar nuevas visualizaciones

## Flujo de Datos

```
┌──────────────┐
│  CSV Data    │
└──────┬───────┘
       │
       ▼
┌────────────────────────┐
│ src/utils/data_loader  │
│ - load_fitness_data()  │
│ - filter_data_by_date()│
└──────┬─────────────────┘
       │
       ▼
┌─────────────────────────────┐
│  App (app_main.py)          │
│  - Inicializa Dash          │
│  - Carga datos globales     │
│  - Registra callbacks       │
└──────┬──────────────────────┘
       │
       ├─────────────────┬──────────────────┐
       ▼                 ▼                  ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────────┐
│   Layout    │  │  Callbacks  │  │  Visualizations │
│   (UI)      │  │  (Lógica)   │  │   (Gráficos)    │
└─────────────┘  └─────────────┘  └─────────────────┘
       │                 │                  │
       └────────┬────────┴──────────────────┘
                ▼
       ┌─────────────────┐
       │  Usuario ve el  │
       │   Dashboard     │
       └─────────────────┘
```

## Estructura de Capas

### 1️⃣ Capa de Configuración (`config/`)
**Responsabilidad**: Configuración global centralizada

- `settings.py`: 
  - Rutas de archivos
  - Puertos de servidores
  - Paleta de colores
  - Objetivos de fitness
  - Estilos CSS compartidos

**Ventajas**:
- Un solo lugar para cambiar configuraciones
- No hardcodear valores mágicos
- Fácil personalización

### 2️⃣ Capa de Utilidades (`src/utils/`)
**Responsabilidad**: Funciones auxiliares reutilizables

- `data_loader.py`:
  - Cargar CSV con manejo de errores
  - Transformaciones de datos
  - Cálculos de métricas derivadas
  - Filtrado y agregaciones

- `formatters.py`:
  - Formateo de números (separadores de miles)
  - Conversiones de unidades
  - Formateo de textos para UI

**Ventajas**:
- DRY (Don't Repeat Yourself)
- Fácil testing unitario
- Reutilización en múltiples páginas

### 3️⃣ Capa de Componentes (`src/components/`)
**Responsabilidad**: Componentes UI reutilizables

- `cards.py`:
  - Tarjetas de estadísticas
  - Tarjetas de información
  - Componentes visuales consistentes

- `navigation.py`:
  - Botones de navegación
  - Menús
  - Enlaces entre páginas

**Ventajas**:
- UI consistente
- Cambios centralizados
- Código más legible

### 4️⃣ Capa de Visualizaciones (`src/visualizations/`)
**Responsabilidad**: Funciones que generan gráficos Plotly

- `basic_charts.py`:
  - Gráficos de líneas
  - Gráficos de pastel
  - Gráficos de barras
  - Gráficos combinados

- `advanced_charts.py`:
  - Heatmaps
  - Gráficos predictivos
  - Análisis de tendencias
  - Visualizaciones complejas

**Ventajas**:
- Separación de lógica de visualización
- Fácil agregar nuevos gráficos
- Configuración centralizada (CHART_CONFIG)

### 5️⃣ Capa de Layouts (`src/layouts/`)
**Responsabilidad**: Estructura HTML/Dash de cada página

- `main_layout.py`:
  - Estructura del dashboard principal
  - Composición de componentes
  - Organización de gráficos

- `advanced_layout.py`:
  - Estructura del dashboard avanzado
  - Layout especializado

**Ventajas**:
- Separación de presentación y lógica
- Fácil reorganizar UI
- Código más limpio

### 6️⃣ Capa de Callbacks (`src/callbacks/`)
**Responsabilidad**: Lógica de interactividad

- `main_callbacks.py`:
  - Función `register_main_callbacks(app, df)`
  - Actualiza tarjetas y gráficos
  - Responde a cambios de filtros

- `advanced_callbacks.py`:
  - Función `register_advanced_callbacks(app, df)`
  - Lógica avanzada
  - Rankings y predicciones

**Patrón de Diseño**:
```python
def register_callbacks(app, df):
    @callback(
        Output(...),
        Input(...)
    )
    def update_component(...):
        # 1. Filtrar datos
        filtered_df = filter_data_by_date(df, start, end)
        
        # 2. Calcular métricas
        stats = calculate_stats(filtered_df)
        
        # 3. Generar visualizaciones
        fig = create_chart(filtered_df)
        
        # 4. Retornar actualizaciones
        return stats, fig
```

**Ventajas**:
- Un archivo por página
- Callbacks organizados
- Fácil debugging

### 7️⃣ Capa de Aplicación (raíz)
**Responsabilidad**: Punto de entrada de cada app

- `app_main.py`:
  ```python
  1. Importar configuración
  2. Crear instancia Dash
  3. Cargar datos
  4. Crear layout
  5. Registrar callbacks
  6. Ejecutar servidor
  ```

- `app_advanced.py`:
  - Mismo patrón para dashboard avanzado

**Ventajas**:
- Aplicaciones independientes
- Diferentes puertos
- Código mínimo en app principal

## Patrones de Diseño Utilizados

### 1. **Factory Pattern**
Funciones que crean componentes:
```python
create_stat_card(icon, title, value_id, detail_id)
create_heatmap_calendar(df)
```

### 2. **Strategy Pattern**
Diferentes estrategias de visualización:
```python
# Seleccionar estrategia según tipo de datos
if has_weight_data:
    chart = create_weight_trend_chart(df)
else:
    chart = create_empty_chart()
```

### 3. **Dependency Injection**
Pasar dependencias explícitamente:
```python
register_main_callbacks(app, df)  # Inyectar app y datos
```

### 4. **Separation of Concerns**
Cada módulo tiene una responsabilidad única:
- `data_loader`: Solo carga datos
- `formatters`: Solo formatea
- `callbacks`: Solo lógica de interacción

## Ventajas de esta Arquitectura

### ✅ Mantenibilidad
- Cambiar un gráfico: Solo editar `visualizations/`
- Cambiar colores: Solo editar `config/settings.py`
- Agregar página: Crear layout + callbacks + app

### ✅ Testabilidad
Cada función es testeable independientemente:
```python
def test_load_data():
    df = load_fitness_data()
    assert len(df) > 0
    assert 'Fecha' in df.columns

def test_format_number():
    assert format_number(1000) == "1,000"
```

### ✅ Escalabilidad
Agregar nueva visualización:
1. Crear función en `visualizations/`
2. Agregar al layout
3. Agregar al callback
4. ¡Listo!

### ✅ Reutilización
```python
# Mismo componente en múltiples páginas
from src.components.cards import create_stat_card

# En main_layout.py
card1 = create_stat_card("👣", "Pasos", ...)

# En advanced_layout.py
card2 = create_stat_card("👣", "Pasos", ...)
```

### ✅ Colaboración
- Frontend dev: Trabaja en `layouts/` y `components/`
- Data scientist: Trabaja en `visualizations/` y `utils/`
- Backend dev: Trabaja en `data_loader` y `callbacks/`

## Flujo de Trabajo para Nuevas Features

### Agregar Nueva Visualización

1. **Crear función de gráfico**:
   ```python
   # src/visualizations/basic_charts.py
   def create_my_new_chart(df):
       fig = go.Figure(...)
       return fig
   ```

2. **Agregar al layout**:
   ```python
   # src/layouts/main_layout.py
   dcc.Graph(id='my-new-chart', ...)
   ```

3. **Agregar al callback**:
   ```python
   # src/callbacks/main_callbacks.py
   @callback(
       Output('my-new-chart', 'figure'),
       ...
   )
   def update_dashboard(...):
       new_fig = create_my_new_chart(filtered_df)
       return ..., new_fig
   ```

### Agregar Nueva Página

1. **Crear layout**: `src/layouts/new_page_layout.py`
2. **Crear callbacks**: `src/callbacks/new_page_callbacks.py`
3. **Crear app**: `app_new_page.py`
4. **Agregar navegación**: Actualizar `src/components/navigation.py`

## Mejores Prácticas

### 📝 Documentación
- Docstrings en todas las funciones
- Comentarios explicativos en lógica compleja
- README actualizado

### 🎨 Estilo de Código
- Nombres descriptivos
- Funciones cortas (< 50 líneas)
- Evitar código duplicado

### 🔧 Configuración
- No hardcodear valores
- Usar `config/settings.py`
- Variables de entorno para datos sensibles

### 📦 Imports
- Imports absolutos desde raíz:
  ```python
  from config.settings import COLORS
  from src.utils.data_loader import load_fitness_data
  ```

## Convenciones de Nombres

### Archivos
- `snake_case.py`: Módulos Python
- `PascalCase` no se usa (solo clases si las hubiera)

### Funciones
- `create_*`: Funciones que crean componentes
- `register_*`: Funciones que registran callbacks
- `calculate_*`: Funciones que calculan métricas
- `format_*`: Funciones que formatean datos

### Variables
- `df`: DataFrame principal
- `filtered_df`: DataFrame filtrado
- `fig`: Objeto Figure de Plotly
- `*_data`: Datos procesados para un propósito específico

## Próximos Pasos

### Mejoras Sugeridas
1. **Testing**: Agregar `tests/` con pytest
2. **CI/CD**: GitHub Actions para testing automático
3. **Docker**: Containerización para deployment
4. **Database**: Migrar de CSV a PostgreSQL
5. **API**: Crear API REST con FastAPI
6. **Cache**: Agregar cache con Redis para datos procesados

---

Esta arquitectura proporciona una base sólida para crecer y mantener el proyecto a largo plazo.
