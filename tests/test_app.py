# tests/test_app.py
import pytest
import os
import json
from app.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clean_data():
    """Limpia los datos antes de cada prueba"""
    if os.path.exists('todos.json'):
        os.remove('todos.json')
    yield
    # Limpiar después de cada prueba
    if os.path.exists('todos.json'):
        os.remove('todos.json')


def test_index_get(client):
    """Prueba obtener la página principal"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data
    assert b'To-Do List' in response.data


def test_health_endpoint(client):
    """Prueba el endpoint de salud"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.data.decode() == 'OK'


def test_add_todo_form(client):
    """Prueba agregar una tarea desde el formulario HTML"""
    response = client.post('/add', data={
        'title': 'Tarea de prueba',
        'description': 'Descripción de prueba',
        'priority': 'alta',
        'due_date': '2024-12-31'
    })
    assert response.status_code == 302  # Redirect
    
    # Verificar que la tarea se creó
    response = client.get('/')
    assert b'Tarea de prueba' in response.data


def test_add_todo_empty_title(client):
    """Prueba agregar una tarea con título vacío"""
    response = client.post('/add', data={
        'title': '',
        'description': 'Descripción',
        'priority': 'media'
    })
    assert response.status_code == 302  # Redirect
    
    # Verificar que no se creó la tarea
    response = client.get('/')
    assert b'Descripcion' not in response.data


def test_update_todo_status_form(client):
    """Prueba actualizar el estado de una tarea desde formulario"""
    # Crear una tarea primero
    client.post('/add', data={
        'title': 'Tarea para actualizar',
        'description': 'Descripción',
        'priority': 'media'
    })
    
    # Marcar como completada
    response = client.post('/update/1', data={'status': 'completada'})
    assert response.status_code == 302  # Redirect
    
    # Verificar que se actualizó
    response = client.get('/')
    assert b'Tarea para actualizar' in response.data


def test_delete_todo_form(client):
    """Prueba eliminar una tarea desde formulario"""
    # Crear una tarea primero
    client.post('/add', data={
        'title': 'Tarea para eliminar',
        'description': 'Descripción',
        'priority': 'media'
    })
    
    # Eliminar la tarea
    response = client.post('/delete/1')
    assert response.status_code == 302  # Redirect
    
    # Verificar que se eliminó
    response = client.get('/')
    assert b'Tarea para eliminar' not in response.data


def test_delete_nonexistent_todo(client):
    """Prueba eliminar una tarea que no existe"""
    response = client.post('/delete/999')
    assert response.status_code == 302  # Redirect


def test_api_get_todos(client):
    """Prueba la API para obtener todas las tareas"""
    response = client.get('/api/todos')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'todos' in data


def test_api_create_todo(client):
    """Prueba la API para crear una tarea"""
    todo_data = {
        'title': 'API Tarea',
        'description': 'Descripción API',
        'priority': 'alta',
        'due_date': '2024-12-31'
    }
    
    response = client.post('/api/todos', 
                          data=json.dumps(todo_data),
                          content_type='application/json')
    assert response.status_code == 201
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['todo']['title'] == 'API Tarea'
    assert data['todo']['priority'] == 'alta'


def test_api_create_todo_empty_title(client):
    """Prueba la API para crear una tarea con título vacío"""
    todo_data = {
        'title': '',
        'description': 'Descripción',
        'priority': 'media'
    }
    
    response = client.post('/api/todos', 
                          data=json.dumps(todo_data),
                          content_type='application/json')
    assert response.status_code == 400
    
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'error' in data


def test_api_get_todo_by_id(client):
    """Prueba la API para obtener una tarea por ID"""
    # Crear una tarea primero
    client.post('/api/todos', 
                data=json.dumps({'title': 'Tarea API', 'priority': 'media'}),
                content_type='application/json')
    
    response = client.get('/api/todos/1')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['todo']['title'] == 'Tarea API'


def test_api_get_todo_by_id_not_found(client):
    """Prueba la API para obtener una tarea que no existe"""
    response = client.get('/api/todos/999')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'error' in data


def test_api_update_todo(client):
    """Prueba la API para actualizar una tarea"""
    # Crear una tarea primero
    client.post('/api/todos', 
                data=json.dumps({'title': 'Tarea Original', 'priority': 'media'}),
                content_type='application/json')
    
    update_data = {
        'title': 'Tarea Actualizada',
        'priority': 'alta',
        'status': 'completada'
    }
    
    response = client.put('/api/todos/1', 
                         data=json.dumps(update_data),
                         content_type='application/json')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['todo']['title'] == 'Tarea Actualizada'
    assert data['todo']['priority'] == 'alta'
    assert data['todo']['status'] == 'completada'


def test_api_update_todo_not_found(client):
    """Prueba la API para actualizar una tarea que no existe"""
    update_data = {'title': 'Nueva Tarea'}
    
    response = client.put('/api/todos/999', 
                         data=json.dumps(update_data),
                         content_type='application/json')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert data['success'] is False


def test_api_delete_todo(client):
    """Prueba la API para eliminar una tarea"""
    # Crear una tarea primero
    client.post('/api/todos', 
                data=json.dumps({'title': 'Tarea para eliminar', 'priority': 'media'}),
                content_type='application/json')
    
    response = client.delete('/api/todos/1')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True


def test_api_delete_todo_not_found(client):
    """Prueba la API para eliminar una tarea que no existe"""
    response = client.delete('/api/todos/999')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert data['success'] is False


def test_api_get_todos_by_status(client):
    """Prueba la API para obtener tareas por estado"""
    # Crear algunas tareas
    client.post('/api/todos', 
                data=json.dumps({'title': 'Tarea 1', 'priority': 'media'}),
                content_type='application/json')
    client.post('/api/todos', 
                data=json.dumps({'title': 'Tarea 2', 'priority': 'alta'}),
                content_type='application/json')
    
    # Marcar una como completada
    client.put('/api/todos/1', 
              data=json.dumps({'status': 'completada'}),
              content_type='application/json')
    
    # Obtener tareas pendientes
    response = client.get('/api/todos/status/pendiente')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert len(data['todos']) == 1
    assert data['todos'][0]['title'] == 'Tarea 2'
    
    # Obtener tareas completadas
    response = client.get('/api/todos/status/completada')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert len(data['todos']) == 1
    assert data['todos'][0]['title'] == 'Tarea 1'


def test_api_get_todos_by_priority(client):
    """Prueba la API para obtener tareas por prioridad"""
    # Crear tareas con diferentes prioridades
    client.post('/api/todos', 
                data=json.dumps({'title': 'Tarea Alta', 'priority': 'alta'}),
                content_type='application/json')
    client.post('/api/todos', 
                data=json.dumps({'title': 'Tarea Media', 'priority': 'media'}),
                content_type='application/json')
    client.post('/api/todos', 
                data=json.dumps({'title': 'Tarea Alta 2', 'priority': 'alta'}),
                content_type='application/json')
    
    # Obtener tareas de alta prioridad
    response = client.get('/api/todos/priority/alta')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert len(data['todos']) == 2
    assert all(todo['priority'] == 'alta' for todo in data['todos'])


def test_api_get_stats(client):
    """Prueba la API para obtener estadísticas"""
    # Crear algunas tareas
    client.post('/api/todos', 
                data=json.dumps({'title': 'Tarea 1', 'priority': 'media'}),
                content_type='application/json')
    client.post('/api/todos', 
                data=json.dumps({'title': 'Tarea 2', 'priority': 'alta'}),
                content_type='application/json')
    
    # Marcar una como completada
    client.put('/api/todos/1', 
              data=json.dumps({'status': 'completada'}),
              content_type='application/json')
    
    response = client.get('/api/stats')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['stats']['total'] == 2
    assert data['stats']['completed'] == 1
    assert data['stats']['pending'] == 1


def test_api_get_overdue_todos(client):
    """Prueba la API para obtener tareas vencidas"""
    from datetime import datetime, timedelta
    
    # Crear una tarea vencida
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    client.post('/api/todos', 
                data=json.dumps({
                    'title': 'Tarea Vencida', 
                    'priority': 'media',
                    'due_date': yesterday
                }),
                content_type='application/json')
    
    response = client.get('/api/overdue')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert len(data['todos']) == 1
    assert data['todos'][0]['title'] == 'Tarea Vencida'


def test_api_invalid_status(client):
    """Prueba la API con estado inválido"""
    response = client.get('/api/todos/status/invalid')
    assert response.status_code == 400
    
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'error' in data


def test_api_invalid_priority(client):
    """Prueba la API con prioridad inválida"""
    response = client.get('/api/todos/priority/invalid')
    assert response.status_code == 400
    
    data = json.loads(response.data)
    assert data['success'] is False
    assert 'error' in data