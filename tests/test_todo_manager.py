# tests/test_todo_manager.py
import pytest
import os
import json
from datetime import datetime, timedelta
from app.todo_manager import (
    TodoManager, create_todo, get_all_todos, get_todo_by_id, 
    update_todo, delete_todo, get_todos_by_status, get_todos_by_priority,
    get_overdue_todos, get_stats
)


@pytest.fixture
def todo_manager():
    """Fixture que crea un TodoManager limpio para cada prueba"""
    manager = TodoManager()
    manager.todos = []
    manager.next_id = 1
    # Limpiar archivo de datos si existe
    if os.path.exists('todos.json'):
        os.remove('todos.json')
    return manager


def test_create_todo_valid(todo_manager):
    """Prueba crear una tarea válida"""
    todo = todo_manager.create_todo("Tarea de prueba", "Descripción de prueba", "media")
    
    assert todo["id"] == 1
    assert todo["title"] == "Tarea de prueba"
    assert todo["description"] == "Descripción de prueba"
    assert todo["priority"] == "media"
    assert todo["status"] == "pendiente"
    assert todo["created_at"] is not None
    assert todo["completed_at"] is None


def test_create_todo_empty_title(todo_manager):
    """Prueba crear una tarea con título vacío"""
    with pytest.raises(ValueError, match="El título de la tarea no puede estar vacío"):
        todo_manager.create_todo("", "Descripción", "media")


def test_create_todo_invalid_priority(todo_manager):
    """Prueba crear una tarea con prioridad inválida"""
    with pytest.raises(ValueError, match="La prioridad debe ser: baja, media o alta"):
        todo_manager.create_todo("Tarea", "Descripción", "invalid")


def test_get_all_todos(todo_manager):
    """Prueba obtener todas las tareas"""
    todo1 = todo_manager.create_todo("Tarea 1", "", "alta")
    todo2 = todo_manager.create_todo("Tarea 2", "", "baja")
    
    todos = todo_manager.get_all_todos()
    assert len(todos) == 2
    assert todos[0]["title"] == "Tarea 1"
    assert todos[1]["title"] == "Tarea 2"


def test_get_todo_by_id(todo_manager):
    """Prueba obtener una tarea por ID"""
    todo = todo_manager.create_todo("Tarea de prueba", "", "media")
    
    found_todo = todo_manager.get_todo_by_id(1)
    assert found_todo is not None
    assert found_todo["title"] == "Tarea de prueba"
    
    not_found = todo_manager.get_todo_by_id(999)
    assert not_found is None


def test_update_todo_valid(todo_manager):
    """Prueba actualizar una tarea válida"""
    todo = todo_manager.create_todo("Tarea original", "Descripción original", "media")
    
    updated_todo = todo_manager.update_todo(1, title="Tarea actualizada", priority="alta")
    
    assert updated_todo["title"] == "Tarea actualizada"
    assert updated_todo["priority"] == "alta"
    assert updated_todo["description"] == "Descripción original"


def test_update_todo_status_to_completed(todo_manager):
    """Prueba marcar una tarea como completada"""
    todo = todo_manager.create_todo("Tarea", "", "media")
    
    updated_todo = todo_manager.update_todo(1, status="completada")
    
    assert updated_todo["status"] == "completada"
    assert updated_todo["completed_at"] is not None


def test_update_todo_status_to_pending(todo_manager):
    """Prueba marcar una tarea como pendiente"""
    todo = todo_manager.create_todo("Tarea", "", "media")
    todo_manager.update_todo(1, status="completada")
    
    updated_todo = todo_manager.update_todo(1, status="pendiente")
    
    assert updated_todo["status"] == "pendiente"
    assert updated_todo["completed_at"] is None


def test_update_todo_empty_title(todo_manager):
    """Prueba actualizar una tarea con título vacío"""
    todo = todo_manager.create_todo("Tarea", "", "media")
    
    with pytest.raises(ValueError, match="El título de la tarea no puede estar vacío"):
        todo_manager.update_todo(1, title="   ")  # Solo espacios en blanco


def test_update_todo_invalid_status(todo_manager):
    """Prueba actualizar una tarea con estado inválido"""
    todo = todo_manager.create_todo("Tarea", "", "media")
    
    with pytest.raises(ValueError, match="El estado debe ser: pendiente o completada"):
        todo_manager.update_todo(1, status="invalid")


def test_update_todo_not_found(todo_manager):
    """Prueba actualizar una tarea que no existe"""
    result = todo_manager.update_todo(999, title="Nueva tarea")
    assert result is None


def test_delete_todo(todo_manager):
    """Prueba eliminar una tarea"""
    todo = todo_manager.create_todo("Tarea", "", "media")
    
    success = todo_manager.delete_todo(1)
    assert success is True
    
    todos = todo_manager.get_all_todos()
    assert len(todos) == 0


def test_delete_todo_not_found(todo_manager):
    """Prueba eliminar una tarea que no existe"""
    success = todo_manager.delete_todo(999)
    assert success is False


def test_get_todos_by_status(todo_manager):
    """Prueba obtener tareas por estado"""
    todo1 = todo_manager.create_todo("Tarea 1", "", "media")
    todo2 = todo_manager.create_todo("Tarea 2", "", "alta")
    todo_manager.update_todo(1, status="completada")
    
    pending_todos = todo_manager.get_todos_by_status("pendiente")
    completed_todos = todo_manager.get_todos_by_status("completada")
    
    assert len(pending_todos) == 1
    assert len(completed_todos) == 1
    assert pending_todos[0]["title"] == "Tarea 2"
    assert completed_todos[0]["title"] == "Tarea 1"


def test_get_todos_by_status_invalid(todo_manager):
    """Prueba obtener tareas con estado inválido"""
    with pytest.raises(ValueError, match="El estado debe ser: pendiente o completada"):
        todo_manager.get_todos_by_status("invalid")


def test_get_todos_by_priority(todo_manager):
    """Prueba obtener tareas por prioridad"""
    todo1 = todo_manager.create_todo("Tarea 1", "", "alta")
    todo2 = todo_manager.create_todo("Tarea 2", "", "baja")
    todo3 = todo_manager.create_todo("Tarea 3", "", "alta")
    
    high_priority = todo_manager.get_todos_by_priority("alta")
    low_priority = todo_manager.get_todos_by_priority("baja")
    
    assert len(high_priority) == 2
    assert len(low_priority) == 1
    assert high_priority[0]["title"] == "Tarea 1"
    assert high_priority[1]["title"] == "Tarea 3"
    assert low_priority[0]["title"] == "Tarea 2"


def test_get_todos_by_priority_invalid(todo_manager):
    """Prueba obtener tareas con prioridad inválida"""
    with pytest.raises(ValueError, match="La prioridad debe ser: baja, media o alta"):
        todo_manager.get_todos_by_priority("invalid")


def test_get_overdue_todos(todo_manager):
    """Prueba obtener tareas vencidas"""
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    todo1 = todo_manager.create_todo("Tarea vencida", "", "media", yesterday)
    todo2 = todo_manager.create_todo("Tarea futura", "", "media", tomorrow)
    todo3 = todo_manager.create_todo("Tarea sin fecha", "", "media")
    
    overdue_todos = todo_manager.get_overdue_todos()
    
    assert len(overdue_todos) == 1
    assert overdue_todos[0]["title"] == "Tarea vencida"


def test_get_stats(todo_manager):
    """Prueba obtener estadísticas"""
    todo1 = todo_manager.create_todo("Tarea 1", "", "alta")
    todo2 = todo_manager.create_todo("Tarea 2", "", "media")
    todo3 = todo_manager.create_todo("Tarea 3", "", "baja")
    
    todo_manager.update_todo(1, status="completada")
    
    stats = todo_manager.get_stats()
    
    assert stats["total"] == 3
    assert stats["completed"] == 1
    assert stats["pending"] == 2
    assert stats["overdue"] == 0
    assert stats["completion_rate"] == pytest.approx(33.33, rel=1e-2)


def test_get_stats_empty(todo_manager):
    """Prueba obtener estadísticas cuando no hay tareas"""
    stats = todo_manager.get_stats()
    
    assert stats["total"] == 0
    assert stats["completed"] == 0
    assert stats["pending"] == 0
    assert stats["overdue"] == 0
    assert stats["completion_rate"] == 0


def test_save_and_load_todos(todo_manager):
    """Prueba guardar y cargar tareas desde archivo"""
    todo1 = todo_manager.create_todo("Tarea 1", "", "alta")
    todo2 = todo_manager.create_todo("Tarea 2", "", "media")
    
    # Crear un nuevo manager que debería cargar los datos
    new_manager = TodoManager()
    
    todos = new_manager.get_all_todos()
    assert len(todos) == 2
    assert todos[0]["title"] == "Tarea 1"
    assert todos[1]["title"] == "Tarea 2"
    assert new_manager.next_id == 3


# Pruebas para las funciones de conveniencia
def test_convenience_functions(todo_manager):
    """Prueba las funciones de conveniencia"""
    # Limpiar datos existentes
    todo_manager.todos = []
    todo_manager.next_id = 1
    
    # Probar funciones de conveniencia
    todo = create_todo("Tarea", "Descripción", "alta")
    assert todo["title"] == "Tarea"
    
    todos = get_all_todos()
    assert len(todos) == 1
    
    found_todo = get_todo_by_id(1)
    assert found_todo["title"] == "Tarea"
    
    updated = update_todo(1, status="completada")
    assert updated["status"] == "completada"
    
    success = delete_todo(1)
    assert success is True
    
    todos = get_all_todos()
    assert len(todos) == 0
