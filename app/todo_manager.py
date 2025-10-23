import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class TodoManager:
    """Manager class for To-Do List operations"""

    def __init__(self, data_file: str = "todos.json"):
        self.data_file = data_file
        self.todos = self._load_todos()

    def _load_todos(self) -> List[Dict]:
        """Load todos from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("todos", [])
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []

    def _save_todos(self):
        """Save todos to JSON file"""
        data = {"todos": self.todos, "next_id": self._get_next_id()}
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _get_next_id(self) -> int:
        """Get next available ID"""
        if not self.todos:
            return 1
        return max(todo.get("id", 0) for todo in self.todos) + 1

    def create_todo(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        due_date: str = "",
        status: str = "pending",
    ) -> Dict:
        """Create a new todo item"""
        if not title.strip():
            raise ValueError("Title cannot be empty")

        todo = {
            "id": self._get_next_id(),
            "title": title.strip(),
            "description": description.strip(),
            "status": (
                status.lower()
                if status.lower() in ["pending", "completed", "in_progress"]
                else "pending"
            ),
            "priority": (
                priority.lower()
                if priority.lower() in ["low", "medium", "high"]
                else "medium"
            ),
            "due_date": due_date,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        self.todos.append(todo)
        self._save_todos()
        return todo

    def get_all_todos(self) -> List[Dict]:
        """Get all todo items"""
        return self.todos.copy()

    def get_todo_by_id(self, todo_id: int) -> Optional[Dict]:
        """Get a specific todo by ID"""
        for todo in self.todos:
            if todo.get("id") == todo_id:
                return todo.copy()
        return None

    def update_todo(
        self,
        todo_id: int,
        title: str = None,
        description: str = None,
        status: str = None,
        priority: str = None,
        due_date: str = None,
    ) -> Optional[Dict]:
        """Update a todo item"""
        for todo in self.todos:
            if todo.get("id") == todo_id:
                if title is not None:
                    if not title.strip():
                        raise ValueError("Title cannot be empty")
                    todo["title"] = title.strip()

                if description is not None:
                    todo["description"] = description.strip()

                if status is not None and status.lower() in [
                    "pending",
                    "completed",
                    "in_progress",
                ]:
                    todo["status"] = status.lower()

                if priority is not None and priority.lower() in [
                    "low",
                    "medium",
                    "high",
                ]:
                    todo["priority"] = priority.lower()

                if due_date is not None:
                    todo["due_date"] = due_date

                todo["updated_at"] = datetime.now().isoformat()
                self._save_todos()
                return todo.copy()

        return None

    def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo item"""
        for i, todo in enumerate(self.todos):
            if todo.get("id") == todo_id:
                del self.todos[i]
                self._save_todos()
                return True
        return False

    def get_todos_by_status(self, status: str) -> List[Dict]:
        """Get todos filtered by status"""
        return [todo for todo in self.todos if todo.get("status") == status.lower()]

    def get_todos_by_priority(self, priority: str) -> List[Dict]:
        """Get todos filtered by priority"""
        return [todo for todo in self.todos if todo.get("priority") == priority.lower()]

    def get_stats(self) -> Dict:
        """Get statistics about todos"""
        total = len(self.todos)
        pending = len(self.get_todos_by_status("pending"))
        completed = len(self.get_todos_by_status("completed"))
        in_progress = len(self.get_todos_by_status("in_progress"))

        return {
            "total": total,
            "pending": pending,
            "completed": completed,
            "in_progress": in_progress,
            "completion_rate": round((completed / total * 100) if total > 0 else 0, 2),
        }

    def get_overdue_todos(self) -> List[Dict]:
        """Get todos that are overdue"""
        overdue = []
        today = datetime.now().date()

        for todo in self.todos:
            if todo.get("due_date") and todo.get("status") != "completed":
                try:
                    due_date = datetime.fromisoformat(todo["due_date"]).date()
                    if due_date < today:
                        overdue.append(todo)
                except ValueError:
                    continue

        return overdue

    def clear_all_todos(self):
        """Clear all todos (for testing purposes)"""
        self.todos = []
        self._save_todos()
