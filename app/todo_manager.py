"""
Gestor de tareas To-Do List
Funciones para crear, leer, actualizar y eliminar tareas
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
import os


class TodoManager:
    """Gestor de tareas con almacenamiento en memoria"""
    
    def __init__(self):
        self.todos = []
        self.next_id = 1
        self.load_todos()
    
    def load_todos(self):
        """Carga las tareas desde archivo JSON si existe"""
        try:
            if os.path.exists('todos.json'):
                with open('todos.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.todos = data.get('todos', [])
                    self.next_id = data.get('next_id', 1)
        except Exception:
            self.todos = []
            self.next_id = 1
    
    def save_todos(self):
        """Guarda las tareas en archivo JSON"""
        try:
            data = {
                'todos': self.todos,
                'next_id': self.next_id
            }
            with open('todos.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass  # En caso de error, continuar sin guardar
    
    def create_todo(self, title: str, description: str = "", priority: str = "media", due_date: str = None) -> Dict:
        """Crea una nueva tarea"""
        if not title or not title.strip():
            raise ValueError("El título de la tarea no puede estar vacío")
        
        if priority not in ["baja", "media", "alta"]:
            raise ValueError("La prioridad debe ser: baja, media o alta")
        
        todo = {
            "id": self.next_id,
            "title": title.strip(),
            "description": description.strip(),
            "priority": priority,
            "status": "pendiente",
            "created_at": datetime.now().isoformat(),
            "due_date": due_date,
            "completed_at": None
        }
        
        self.todos.append(todo)
        self.next_id += 1
        self.save_todos()
        return todo
    
    def get_all_todos(self) -> List[Dict]:
        """Obtiene todas las tareas"""
        return self.todos.copy()
    
    def get_todo_by_id(self, todo_id: int) -> Optional[Dict]:
        """Obtiene una tarea por su ID"""
        for todo in self.todos:
            if todo["id"] == todo_id:
                return todo
        return None
    
    def update_todo(self, todo_id: int, **kwargs) -> Optional[Dict]:
        """Actualiza una tarea existente"""
        todo = self.get_todo_by_id(todo_id)
        if not todo:
            return None
        
        # Validaciones
        if "title" in kwargs and kwargs["title"]:
            if not kwargs["title"].strip():
                raise ValueError("El título de la tarea no puede estar vacío")
            todo["title"] = kwargs["title"].strip()
        
        if "priority" in kwargs:
            if kwargs["priority"] not in ["baja", "media", "alta"]:
                raise ValueError("La prioridad debe ser: baja, media o alta")
            todo["priority"] = kwargs["priority"]
        
        if "status" in kwargs:
            if kwargs["status"] not in ["pendiente", "completada"]:
                raise ValueError("El estado debe ser: pendiente o completada")
            todo["status"] = kwargs["status"]
            if kwargs["status"] == "completada":
                todo["completed_at"] = datetime.now().isoformat()
            else:
                todo["completed_at"] = None
        
        if "description" in kwargs:
            todo["description"] = kwargs["description"].strip()
        
        if "due_date" in kwargs:
            todo["due_date"] = kwargs["due_date"]
        
        self.save_todos()
        return todo
    
    def delete_todo(self, todo_id: int) -> bool:
        """Elimina una tarea"""
        for i, todo in enumerate(self.todos):
            if todo["id"] == todo_id:
                del self.todos[i]
                self.save_todos()
                return True
        return False
    
    def get_todos_by_status(self, status: str) -> List[Dict]:
        """Obtiene tareas filtradas por estado"""
        if status not in ["pendiente", "completada"]:
            raise ValueError("El estado debe ser: pendiente o completada")
        return [todo for todo in self.todos if todo["status"] == status]
    
    def get_todos_by_priority(self, priority: str) -> List[Dict]:
        """Obtiene tareas filtradas por prioridad"""
        if priority not in ["baja", "media", "alta"]:
            raise ValueError("La prioridad debe ser: baja, media o alta")
        return [todo for todo in self.todos if todo["priority"] == priority]
    
    def get_overdue_todos(self) -> List[Dict]:
        """Obtiene tareas vencidas"""
        now = datetime.now()
        overdue = []
        for todo in self.todos:
            if todo["due_date"] and todo["status"] == "pendiente":
                try:
                    due_date = datetime.fromisoformat(todo["due_date"])
                    if due_date < now:
                        overdue.append(todo)
                except ValueError:
                    continue
        return overdue
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas de las tareas"""
        total = len(self.todos)
        completed = len([t for t in self.todos if t["status"] == "completada"])
        pending = total - completed
        overdue = len(self.get_overdue_todos())
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "overdue": overdue,
            "completion_rate": (completed / total * 100) if total > 0 else 0
        }


# Instancia global del gestor de tareas
todo_manager = TodoManager()


# Funciones de conveniencia para compatibilidad con la API
def create_todo(title: str, description: str = "", priority: str = "media", due_date: str = None) -> Dict:
    """Crea una nueva tarea"""
    return todo_manager.create_todo(title, description, priority, due_date)


def get_all_todos() -> List[Dict]:
    """Obtiene todas las tareas"""
    return todo_manager.get_all_todos()


def get_todo_by_id(todo_id: int) -> Optional[Dict]:
    """Obtiene una tarea por su ID"""
    return todo_manager.get_todo_by_id(todo_id)


def update_todo(todo_id: int, **kwargs) -> Optional[Dict]:
    """Actualiza una tarea existente"""
    return todo_manager.update_todo(todo_id, **kwargs)


def delete_todo(todo_id: int) -> bool:
    """Elimina una tarea"""
    return todo_manager.delete_todo(todo_id)


def get_todos_by_status(status: str) -> List[Dict]:
    """Obtiene tareas filtradas por estado"""
    return todo_manager.get_todos_by_status(status)


def get_todos_by_priority(priority: str) -> List[Dict]:
    """Obtiene tareas filtradas por prioridad"""
    return todo_manager.get_todos_by_priority(priority)


def get_overdue_todos() -> List[Dict]:
    """Obtiene tareas vencidas"""
    return todo_manager.get_overdue_todos()


def get_stats() -> Dict:
    """Obtiene estadísticas de las tareas"""
    return todo_manager.get_stats()
