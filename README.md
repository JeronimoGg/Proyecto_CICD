# 📝 To-Do List Application

Una aplicación moderna y minimalista de lista de tareas construida con Flask, diseñada para demostrar mejores prácticas de desarrollo, testing y despliegue en la nube.

## 🚀 Características

- **Interfaz moderna y minimalista** con diseño responsivo
- **Gestión completa de tareas** con estados (pendiente, en progreso, completada)
- **Sistema de prioridades** (alta, media, baja)
- **Fechas límite** para tareas
- **Estadísticas en tiempo real** del progreso
- **API RESTful** completa
- **Persistencia de datos** en JSON
- **Tests comprehensivos** (unitarios, integración, aceptación, smoke)
- **CI/CD pipeline** con GitHub Actions
- **Despliegue en AWS** con ECS Fargate y ALB

## 🛠️ Tecnologías

- **Backend**: Python 3.11, Flask
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **Testing**: pytest, Selenium, coverage
- **Containerización**: Docker
- **CI/CD**: GitHub Actions
- **Cloud**: AWS (ECS Fargate, ALB, CloudFormation)
- **Monitoreo**: CloudWatch Logs

## 📦 Instalación

### Prerrequisitos

- Python 3.11+
- pip
- Git

### Pasos de instalación

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
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **Linux/macOS:**
   ```bash
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
   - Abrir navegador en `http://localhost:5000`

## 🧪 Testing

El proyecto incluye cuatro tipos de tests organizados por ramas:

### Tests Unitarios (`dev` branch)
```bash
pytest tests/test_todo_manager.py -v
```

### Tests de Integración (`dev` branch)
```bash
pytest tests/test_app.py -v
```

### Tests de Aceptación (`staging` branch)
```bash
pytest tests/test_acceptance_app.py -v
```

### Tests de Smoke (`main` branch)
```bash
pytest tests/test_smoke_app.py -v
```

### Ejecutar todos los tests
```bash
pytest tests/ -v --cov=app --cov-report=html
```

## 🔌 API Endpoints

### Tareas
- `GET /api/todos` - Obtener todas las tareas
- `GET /api/todos/{id}` - Obtener tarea específica
- `POST /api/todos` - Crear nueva tarea
- `PUT /api/todos/{id}` - Actualizar tarea
- `DELETE /api/todos/{id}` - Eliminar tarea

### Filtros
- `GET /api/todos/status/{status}` - Filtrar por estado
- `GET /api/todos/priority/{priority}` - Filtrar por prioridad
- `GET /api/todos/overdue` - Obtener tareas vencidas

### Estadísticas
- `GET /api/stats` - Obtener estadísticas
- `GET /health` - Health check

### Ejemplo de uso de la API

```bash
# Crear una tarea
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Completar proyecto",
    "description": "Finalizar la documentación",
    "priority": "high",
    "due_date": "2024-12-31"
  }'

# Obtener todas las tareas
curl http://localhost:5000/api/todos

# Obtener estadísticas
curl http://localhost:5000/api/stats
```

## 🐳 Docker

### Construir imagen
```bash
docker build -t todo-list-app .
```

### Ejecutar contenedor
```bash
docker run -p 5000:5000 todo-list-app
```

## ☁️ Despliegue en AWS

### Prerrequisitos
- AWS CLI configurado
- Permisos para ECS, ECR, CloudFormation

### Pasos de despliegue

1. **Crear repositorio ECR**
   ```bash
   aws ecr create-repository --repository-name todo-list-app
   ```

2. **Autenticar Docker con ECR**
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
   ```

3. **Construir y subir imagen**
   ```bash
   docker build -t todo-list-app .
   docker tag todo-list-app:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/todo-list-app:latest
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/todo-list-app:latest
   ```

4. **Desplegar con CloudFormation**
   ```bash
   aws cloudformation create-stack \
     --stack-name todo-list-prod \
     --template-body file://template.yaml \
     --parameters ParameterKey=Environment,ParameterValue=production \
     --capabilities CAPABILITY_IAM
   ```

## 🔄 CI/CD Pipeline

El proyecto utiliza GitHub Actions con un pipeline multi-branch:

### Rama `dev`
- Tests unitarios e integración
- Build de imagen Docker
- Push a ECR con tag `dev`

### Rama `staging`
- Tests de aceptación
- Deploy a ambiente de staging
- Push a ECR con tag `staging`

### Rama `main`
- Tests de smoke
- Deploy a producción
- Push a ECR con tag `latest`

## 📁 Estructura del Proyecto

```
Proyecto_CICD/
├── app/
│   ├── __init__.py
│   ├── app.py              # Aplicación Flask principal
│   ├── todo_manager.py     # Lógica de negocio
│   └── templates/
│       └── index.html      # Frontend
├── tests/
│   ├── test_todo_manager.py    # Tests unitarios
│   ├── test_app.py             # Tests de integración
│   ├── test_acceptance_app.py  # Tests de aceptación
│   └── test_smoke_app.py       # Tests de smoke
├── .github/
│   └── workflows/
│       └── ci-cd.yml       # Pipeline CI/CD
├── Dockerfile              # Configuración Docker
├── template.yaml           # CloudFormation template
├── requirements.txt        # Dependencias Python
├── pytest.ini            # Configuración pytest
├── sonar-project.properties # Configuración SonarQube
├── todos.json             # Datos de la aplicación
└── README.md              # Este archivo
```

## 🎯 Funcionalidades de la Aplicación

### Gestión de Tareas
- ✅ Crear nuevas tareas con título, descripción, prioridad y fecha límite
- ✅ Marcar tareas como completadas
- ✅ Cambiar estado de tareas (pendiente → en progreso → completada)
- ✅ Eliminar tareas
- ✅ Editar tareas existentes

### Características Avanzadas
- 📊 Estadísticas en tiempo real (total, pendientes, completadas, progreso)
- 🔍 Filtrado por estado y prioridad
- ⏰ Detección de tareas vencidas
- 📱 Diseño responsivo para móviles y tablets
- 🎨 Interfaz moderna con gradientes y animaciones

## 🚦 Estados de las Tareas

- **Pendiente** (🟡): Tarea creada pero no iniciada
- **En Progreso** (🔵): Tarea en desarrollo
- **Completada** (🟢): Tarea finalizada

## 🎨 Prioridades

- **Alta** (🔴): Tareas urgentes e importantes
- **Media** (🟡): Tareas importantes pero no urgentes
- **Baja** (🟢): Tareas de baja prioridad

## 🔧 Desarrollo

### Configuración del entorno de desarrollo

1. **Instalar dependencias de desarrollo**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecutar tests en modo watch**
   ```bash
   pytest-watch tests/
   ```

3. **Verificar cobertura de código**
   ```bash
   pytest --cov=app --cov-report=html
   ```

### Convenciones de código

- **PEP 8** para estilo de código Python
- **Docstrings** para documentación de funciones
- **Type hints** para mejor legibilidad
- **Tests** para cada funcionalidad nueva

## 📊 Métricas y Monitoreo

- **Cobertura de código**: >80%
- **Tests**: Unitarios, integración, aceptación, smoke
- **Logs**: CloudWatch Logs para monitoreo
- **Health checks**: Endpoint `/health` para verificación

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte o preguntas, crear un issue en el repositorio de GitHub.

---

**Desarrollado con ❤️ usando Flask, Docker y AWS**