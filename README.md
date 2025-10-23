# 📝 To-Do List Application

Una aplicación web moderna y minimalista para gestionar tareas, desarrollada con Flask y desplegada en AWS ECS Fargate.

## ✨ Características

- **🎨 Diseño moderno y minimalista** con gradientes y animaciones suaves
- **📱 Interfaz responsive** que funciona en desktop y móviles
- **⚡ Operaciones CRUD completas** para gestionar tareas
- **🏷️ Sistema de prioridades** (Baja, Media, Alta)
- **📅 Fechas de vencimiento** para las tareas
- **📊 Estadísticas en tiempo real** del progreso
- **🔄 Estados de tareas** (Pendiente, Completada)
- **💾 Persistencia de datos** en archivo JSON
- **🌐 API REST completa** para integración

## 🚀 Tecnologías

- **Backend**: Python 3.11+ con Flask
- **Frontend**: HTML5, CSS3, JavaScript vanilla
- **Testing**: pytest, Selenium, Coverage
- **CI/CD**: GitHub Actions
- **Cloud**: AWS ECS Fargate, CloudFormation, ALB
- **Containerización**: Docker

## 🛠️ Instalación y Ejecución Local

### Prerrequisitos
- Python 3.11+
- pip

### Pasos

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd Proyecto_CICD
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   ```

3. **Activar entorno virtual**
   ```bash
   # Windows
   .\venv\Scripts\Activate.ps1
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

5. **Ejecutar la aplicación**
   ```bash
   python -m app.app
   ```

6. **Acceder a la aplicación**
   - Abrir navegador en: `http://localhost:5000`

## 🧪 Testing

### Ejecutar todas las pruebas
```bash
pytest tests/ -v
```

### Ejecutar pruebas específicas
```bash
# Pruebas unitarias
pytest tests/test_todo_manager.py -v

# Pruebas de integración
pytest tests/test_app.py -v

# Pruebas de aceptación
pytest tests/test_acceptance_app.py -v

# Pruebas smoke
pytest tests/test_smoke_app.py -v
```

### Generar reporte de cobertura
```bash
pytest --cov=app --cov-report=html
```

## 🐳 Docker

### Construir imagen
```bash
docker build -t todo-list-app .
```

### Ejecutar contenedor
```bash
docker run -p 8000:8000 todo-list-app
```

## ☁️ Despliegue en AWS

La aplicación está configurada para desplegarse automáticamente en AWS usando:

- **ECS Fargate** para el hosting
- **Application Load Balancer** para el tráfico
- **CloudFormation** para la infraestructura
- **GitHub Actions** para CI/CD

### Entornos
- **Staging**: `todo-list-staging-stack`
- **Production**: `todo-list-prod-stack`

## 📋 API Endpoints

### Tareas
- `GET /api/todos` - Obtener todas las tareas
- `POST /api/todos` - Crear nueva tarea
- `GET /api/todos/{id}` - Obtener tarea por ID
- `PUT /api/todos/{id}` - Actualizar tarea
- `DELETE /api/todos/{id}` - Eliminar tarea

### Filtros
- `GET /api/todos/status/{status}` - Filtrar por estado
- `GET /api/todos/priority/{priority}` - Filtrar por prioridad
- `GET /api/overdue` - Obtener tareas vencidas

### Utilidades
- `GET /api/stats` - Obtener estadísticas
- `GET /health` - Health check

## 📁 Estructura del Proyecto

```
Proyecto_CICD/
├── app/
│   ├── __init__.py
│   ├── app.py              # Aplicación Flask principal
│   ├── todo_manager.py     # Gestor de tareas
│   └── templates/
│       └── index.html      # Frontend
├── tests/
│   ├── test_todo_manager.py    # Pruebas unitarias
│   ├── test_app.py             # Pruebas de integración
│   ├── test_acceptance_app.py  # Pruebas de aceptación
│   └── test_smoke_app.py       # Pruebas smoke
├── .github/workflows/
│   └── ci-cd.yml           # Pipeline CI/CD
├── template.yaml            # CloudFormation template
├── Dockerfile              # Configuración Docker
├── requirements.txt        # Dependencias Python
└── README.md              # Este archivo
```

## 🔧 Configuración

### Variables de Entorno
- `PORT`: Puerto de la aplicación (default: 5000)
- `APP_BASE_URL`: URL base para pruebas (default: http://localhost:5000)

### Archivos de Configuración
- `pytest.ini`: Configuración de pruebas
- `sonar-project.properties`: Configuración SonarCloud
- `.gitignore`: Archivos ignorados por Git

## 📊 Métricas de Calidad

- **Cobertura de código**: >85%
- **Pruebas**: Unitarias, integración, aceptación y smoke
- **Linting**: Pylint, Flake8, Black
- **Análisis estático**: SonarCloud

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

Desarrollado como parte del proyecto de integración continua y despliegue continuo (CI/CD).

---

**¡Organiza tus tareas de manera eficiente con esta aplicación moderna!** ✨