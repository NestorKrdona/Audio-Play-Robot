#!/bin/bash

# Ruta al entorno virtual si estás usando uno
# source /home/tu_usuario/venv/bin/activate

# Ruta a tu archivo de aplicación Flask
cd /home/tu_usuario/tu_proyecto

# Ejecutar la aplicación Flask
/usr/bin/python3 app.py >> /home/tu_usuario/tu_proyecto/app.log 2>&1
