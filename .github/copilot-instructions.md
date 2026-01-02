# Fitness Dashboard - AI Agent Instructions

## Project Overview
Interactive Dash/Plotly dashboard for visualizing Google Fit metrics. Single unified app with tab-based navigation (Main Dashboard, Advanced Analysis, Conclusions).

## Architecture Pattern: Clean Modular Dash

### Core Flow
1. **Data Loading** (`src/utils/data_loader.py`): CSV → Pandas DataFrame with computed metrics (velocity, pace, derived dates)
2. **App Initialization** (`app.py`): Single Dash app loads data once globally, creates tab-based layout
3. **Layout Functions** (`src/layouts/`): Return Dash components, accept data/dates as params
4. **Callback Registration** (`src/callbacks/`): `register_*_callbacks(app, df)` pattern - register all callbacks for a section at once
5. **Visualization Functions** (`src/visualizations/`): Pure functions that return Plotly figures

### Critical Patterns

**Never instantiate Dash multiple times** - This is a unified single-app architecture. Old pattern with `app_main.py`, `app_advanced.py`, `conclusiones.py` as separate apps was refactored out.

**Configuration Centralization** (`config/settings.py`):
```python
COLORS = {...}        # All color constants
CHART_CONFIG = {...}  # Plotly layout defaults (includes margin!)
GOALS = {...}         # Fitness targets
DATA_PATH = ...       # Relative path to CSV
```
⚠️ **NEVER pass `margin=` to `fig.update_layout()` when spreading `**CHART_CONFIG`** - causes "multiple values for keyword argument" error.

**Import Pattern for Modules**:
```python
import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))  # or '../..' for nested
from config.settings import COLORS, PORTS
```
All src modules use relative path manipulation for imports.

**Callback Pattern**:
```python
def register_main_callbacks(app, df):
    @callback(Output(...), Input(...))
    def update_function(date_start, date_end):
        filtered_df = filter_data_by_date(df, date_start, date_end)
        # ... compute and return
```
Data filtering happens inside callbacks, original df is immutable global.

## Component Structure

- **Layouts** return complete UI sections with IDs for callbacks
- **Components** (`src/components/`) create reusable UI elements (cards, navigation)
- **Visualizations** are pure functions: `DataFrame → go.Figure`
- **Formatters** (`src/utils/formatters.py`) standardize number display

## Data Conventions

**Google Fit CSV columns** (Spanish):
- `Fecha` (date), `Recuento de pasos` (steps), `Distancia (m)`, `Calorías (kcal)`
- `Recuento de Minutos Activos`, activity durations in ms
- Weight/heart rate columns may be sparse

**Computed columns** (in `load_fitness_data()`):
- `Distancia_km`, `Velocidad_kmh`, `Pace_min_km`
- `Año`, `Mes`, `MesNombre`, `DíaSemana`

## Development Workflow

**Run**: `python app.py` → Opens on port 8050 (set in `config/settings.py`)

**Adding visualizations**:
1. Create function in `src/visualizations/basic_charts.py` or `advanced_charts.py`
2. Add to layout in `src/layouts/*.py` with unique component ID
3. Register callback in `src/callbacks/*.py` to update figure

**New tab/section**:
1. Create layout function in `src/layouts/`
2. Add tab to `app.py` tabs definition
3. Update `render_tab_content` callback to include new tab
4. Create corresponding `register_*_callbacks()` in `src/callbacks/`

## Common Pitfalls

❌ Don't hardcode colors - use `COLORS` dict
❌ Don't create multiple Dash instances
❌ Don't modify `df` in callbacks - use `filter_data_by_date()` 
❌ Don't pass conflicting kwargs with `**CHART_CONFIG`
❌ Don't use absolute paths - `DATA_PATH` uses `os.path.join()` for portability

## Testing After Changes

Run app and verify:
1. All three tabs load without errors
2. Date picker filters update all charts
3. No "multiple values for keyword argument" errors
4. Charts maintain dark theme styling

## Key Files

- `app.py`: Entry point, tab navigation, unified app
- `config/settings.py`: Single source of truth for config
- `src/utils/data_loader.py`: Data preprocessing logic
- `src/callbacks/`: Interactive logic, one file per tab
- `src/visualizations/`: Chart generation, stateless functions
