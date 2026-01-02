"""
WSGI config for PythonAnywhere deployment
"""
import sys
import os

# Agregar el directorio del proyecto al path
project_home = '/home/YOUR_USERNAME/fitness-dashboard'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Importar la aplicación
from app import app

# PythonAnywhere usa 'application' como nombre del objeto WSGI
application = app.server
