# Despliegue en Render.com

## 🚀 Pasos para publicar tu Dashboard

### 1. Preparar el repositorio
Los archivos necesarios ya están configurados:
- ✅ `requirements.txt` - Dependencias actualizadas con gunicorn
- ✅ `render.yaml` - Configuración de Render
- ✅ `app.py` - Ajustado para producción

### 2. Subir cambios a GitHub

```bash
git add .
git commit -m "Add: Configuración para deploy en Render"
git push
```

### 3. Crear cuenta en Render

1. Ve a https://render.com
2. Haz clic en "Get Started for Free"
3. Conecta tu cuenta de GitHub

### 4. Crear nuevo Web Service

1. En el dashboard de Render, haz clic en **"New +"** → **"Web Service"**
2. Conecta tu repositorio `fitness-dashboard`
3. Configura los siguientes valores:

   - **Name**: `fitness-dashboard` (o el nombre que prefieras)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:server`
   - **Plan**: Free

4. Haz clic en **"Create Web Service"**

### 5. Esperar el despliegue

- Render automáticamente:
  - Instalará las dependencias
  - Iniciará tu aplicación
  - Te dará una URL pública (ejemplo: `https://fitness-dashboard-xxxx.onrender.com`)

⏱️ El primer despliegue toma ~5-10 minutos

### 6. Acceder a tu Dashboard

Una vez completado, tu dashboard estará disponible públicamente en la URL proporcionada.

## ⚠️ Limitaciones del plan gratuito

- La app se "duerme" después de 15 minutos de inactividad
- Primera carga después de dormir toma ~30 segundos
- 750 horas gratis al mes

## 🔄 Actualizaciones automáticas

Cada vez que hagas `git push` a tu repositorio, Render automáticamente:
1. Detecta los cambios
2. Redespliega la aplicación
3. Actualiza la URL pública

## 🐛 Troubleshooting

Si hay errores en el despliegue, revisa los logs en el dashboard de Render para ver qué salió mal.
