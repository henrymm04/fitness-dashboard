# Despliegue en PythonAnywhere

## 🚀 Guía Completa de Despliegue

### 1️⃣ Crear cuenta en PythonAnywhere

1. Ve a **https://www.pythonanywhere.com**
2. Clic en **"Pricing & signup"**
3. Selecciona **"Create a Beginner account"** (gratis)
4. Completa el registro

### 2️⃣ Abrir consola Bash

1. En el Dashboard, ve a la pestaña **"Consoles"**
2. Clic en **"Bash"** para abrir una nueva consola

### 3️⃣ Clonar tu repositorio

En la consola Bash, ejecuta:

```bash
git clone https://github.com/henrymm04/fitness-dashboard.git
cd fitness-dashboard
```

### 4️⃣ Crear y activar entorno virtual

```bash
mkvirtualenv fitness-dashboard --python=/usr/bin/python3.10
workon fitness-dashboard
```

### 5️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 6️⃣ Configurar Web App

1. Ve a la pestaña **"Web"** en el dashboard
2. Clic en **"Add a new web app"**
3. Selecciona **"Manual configuration"**
4. Elige **"Python 3.10"**

### 7️⃣ Configurar archivos en la Web App

#### A. Source code:
```
/home/YOUR_USERNAME/fitness-dashboard
```
Reemplaza `YOUR_USERNAME` con tu nombre de usuario de PythonAnywhere

#### B. Working directory:
```
/home/YOUR_USERNAME/fitness-dashboard
```

#### C. Virtualenv:
```
/home/YOUR_USERNAME/.virtualenvs/fitness-dashboard
```

#### D. WSGI configuration file:

1. Haz clic en el enlace del archivo WSGI (algo como `/var/www/your_username_pythonanywhere_com_wsgi.py`)
2. **Borra todo el contenido** del archivo
3. Pega este código:

```python
import sys
import os

# Reemplaza YOUR_USERNAME con tu nombre de usuario
project_home = '/home/YOUR_USERNAME/fitness-dashboard'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Importar la aplicación
from app import app

# PythonAnywhere usa 'application' como nombre del objeto WSGI
application = app.server
```

4. **Guarda el archivo** (botón verde "Save")

### 8️⃣ Subir los datos

Como los datos en `data/` pueden no estar en GitHub (por .gitignore), súbelos manualmente:

1. Ve a la pestaña **"Files"**
2. Navega a `/home/YOUR_USERNAME/fitness-dashboard/data/`
3. Clic en **"Upload a file"**
4. Sube tu archivo `Daily activity metrics.csv`

### 9️⃣ Iniciar la aplicación

1. Vuelve a la pestaña **"Web"**
2. Haz clic en el botón verde **"Reload your_username.pythonanywhere.com"**
3. Espera unos segundos

### 🔟 Acceder a tu Dashboard

Tu aplicación estará disponible en:
```
https://YOUR_USERNAME.pythonanywhere.com
```

---

## 🔧 Troubleshooting

### Error: "Could not import app"
- Verifica que el path en el archivo WSGI sea correcto
- Asegúrate de haber instalado todas las dependencias
- Revisa los logs en la pestaña "Web" → "Error log"

### Error: "No module named 'pandas'"
```bash
workon fitness-dashboard
pip install -r requirements.txt
```

### La app no carga
1. Ve a "Web" → "Error log" para ver el error específico
2. Verifica que el archivo CSV esté en `data/`
3. Asegúrate de haber hecho "Reload" después de los cambios

### Ver logs en tiempo real
En la consola Bash:
```bash
tail -f /var/log/YOUR_USERNAME.pythonanywhere.com.error.log
```

---

## 🔄 Actualizar la aplicación

Cuando hagas cambios en tu código:

```bash
cd ~/fitness-dashboard
git pull
# Si cambiaste requirements.txt:
workon fitness-dashboard
pip install -r requirements.txt
```

Luego en la pestaña "Web" → **"Reload"**

---

## ⚠️ Limitaciones del plan gratuito

- Un solo web app
- Límite de CPU: 100 segundos/día
- Sin acceso a sitios externos (excepto whitelist)
- La app se desactiva después de 3 meses sin actividad

---

## 📊 Verificar que funciona

Después del deploy, prueba:
1. Abrir la URL de tu app
2. Cambiar entre pestañas (Principal, Avanzado, Conclusiones)
3. Probar los filtros de fecha
4. Verificar que los gráficos cargan correctamente

---

## 🆘 Soporte

Si encuentras problemas:
1. Revisa los logs de error
2. Verifica la consola del navegador (F12)
3. Comprueba que todos los archivos estén en su lugar
