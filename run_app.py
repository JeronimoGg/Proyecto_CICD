#!/usr/bin/env python3
"""
Script simple para ejecutar la app To-Do List
"""
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.getcwd())

# Importar y ejecutar la app
from app.app import app

if __name__ == "__main__":
    print("🚀 Iniciando To-Do List App...")
    print("📱 Abre tu navegador en: http://localhost:5000")
    print("⏹️  Presiona Ctrl+C para detener")
    app.run(debug=True, host='0.0.0.0', port=5000)
