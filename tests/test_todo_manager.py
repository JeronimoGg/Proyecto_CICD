import pytest
import json
import os
from datetime import datetime
from app.todo_manager import TodoManager


class TestTodoManager:
    """Test cases for TodoManager class"""
    
    def setup_method(self):
        """Setup method run before each test"""
        self.test_file = "test_todos.json"
        self.todo_manager = TodoManager(self.test_file)
        self.todo_manager.clear_all_todos()
    
    def teardown_method(self):
        """Cleanup method run after each test"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_create_todo_success(self):
        """Test creating a todo successfully"""
        todo = self.todo_manager.create_todo("Test task", "Test description", "high", "2024-12-31")
        
        assert todo['title'] == "Test task"
        assert todo['description'] == "Test description"
        assert todo['priority'] == "high"
        assert todo['due_date'] == "2024-12-31"
        assert todo['status'] == "pending"
        assert 'id' in todo
        assert 'created_at' in todo
        assert 'updated_at' in todo
    
    def test_create_todo_empty_title(self):
        """Test creating a todo with empty title raises ValueError"""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            self.todo_manager.create_todo("")
    
    def test_create_todo_whitespace_title(self):
        """Test creating a todo with whitespace-only title raises ValueError"""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            self.todo_manager.create_todo("   ")
    
    def test_create_todo_invalid_priority(self):
        """Test creating a todo with invalid priority defaults to medium"""
        todo = self.todo_manager.create_todo("Test task", priority="invalid")
        assert todo['priority'] == "medium"
    
    def test_get_all_todos(self):
        """Test getting all todos"""
        # Initially empty
        assert len(self.todo_manager.get_all_todos()) == 0
        
        # Add some todos
        self.todo_manager.create_todo("Task 1")
        self.todo_manager.create_todo("Task 2")
        
        todos = self.todo_manager.get_all_todos()
        assert len(todos) == 2
        assert todos[0]['title'] == "Task 1"
        assert todos[1]['title'] == "Task 2"
    
    def test_get_todo_by_id(self):
        """Test getting a todo by ID"""
        todo = self.todo_manager.create_todo("Test task")
        todo_id = todo['id']
        
        retrieved_todo = self.todo_manager.get_todo_by_id(todo_id)
        assert retrieved_todo is not None
        assert retrieved_todo['title'] == "Test task"
        assert retrieved_todo['id'] == todo_id
    
    def test_get_todo_by_id_not_found(self):
        """Test getting a todo by non-existent ID"""
        result = self.todo_manager.get_todo_by_id(999)
        assert result is None
    
    def test_update_todo_success(self):
        """Test updating a todo successfully"""
        todo = self.todo_manager.create_todo("Original title")
        todo_id = todo['id']
        
        updated_todo = self.todo_manager.update_todo(
            todo_id, 
            title="Updated title",
            description="Updated description",
            status="completed",
            priority="high"
        )
        
        assert updated_todo is not None
        assert updated_todo['title'] == "Updated title"
        assert updated_todo['description'] == "Updated description"
        assert updated_todo['status'] == "completed"
        assert updated_todo['priority'] == "high"
        assert updated_todo['id'] == todo_id
    
    def test_update_todo_empty_title(self):
        """Test updating a todo with empty title raises ValueError"""
        todo = self.todo_manager.create_todo("Original title")
        todo_id = todo['id']
        
        with pytest.raises(ValueError, match="Title cannot be empty"):
            self.todo_manager.update_todo(todo_id, title="")
    
    def test_update_todo_invalid_status(self):
        """Test updating a todo with invalid status is ignored"""
        todo = self.todo_manager.create_todo("Test task")
        todo_id = todo['id']
        
        updated_todo = self.todo_manager.update_todo(todo_id, status="invalid_status")
        assert updated_todo['status'] == "pending"  # Should remain unchanged
    
    def test_update_todo_invalid_priority(self):
        """Test updating a todo with invalid priority is ignored"""
        todo = self.todo_manager.create_todo("Test task")
        todo_id = todo['id']
        
        updated_todo = self.todo_manager.update_todo(todo_id, priority="invalid_priority")
        assert updated_todo['priority'] == "medium"  # Should remain unchanged
    
    def test_update_todo_not_found(self):
        """Test updating a non-existent todo"""
        result = self.todo_manager.update_todo(999, title="Updated")
        assert result is None
    
    def test_delete_todo_success(self):
        """Test deleting a todo successfully"""
        todo = self.todo_manager.create_todo("Test task")
        todo_id = todo['id']
        
        success = self.todo_manager.delete_todo(todo_id)
        assert success is True
        
        # Verify todo is deleted
        assert self.todo_manager.get_todo_by_id(todo_id) is None
        assert len(self.todo_manager.get_all_todos()) == 0
    
    def test_delete_todo_not_found(self):
        """Test deleting a non-existent todo"""
        success = self.todo_manager.delete_todo(999)
        assert success is False
    
    def test_get_todos_by_status(self):
        """Test getting todos filtered by status"""
        self.todo_manager.create_todo("Task 1", status="pending")
        self.todo_manager.create_todo("Task 2", status="completed")
        self.todo_manager.create_todo("Task 3", status="pending")
        
        pending_todos = self.todo_manager.get_todos_by_status("pending")
        completed_todos = self.todo_manager.get_todos_by_status("completed")
        
        assert len(pending_todos) == 2
        assert len(completed_todos) == 1
        assert all(todo['status'] == 'pending' for todo in pending_todos)
        assert all(todo['status'] == 'completed' for todo in completed_todos)
    
    def test_get_todos_by_priority(self):
        """Test getting todos filtered by priority"""
        self.todo_manager.create_todo("Task 1", priority="high")
        self.todo_manager.create_todo("Task 2", priority="low")
        self.todo_manager.create_todo("Task 3", priority="high")
        
        high_priority_todos = self.todo_manager.get_todos_by_priority("high")
        low_priority_todos = self.todo_manager.get_todos_by_priority("low")
        
        assert len(high_priority_todos) == 2
        assert len(low_priority_todos) == 1
        assert all(todo['priority'] == 'high' for todo in high_priority_todos)
        assert all(todo['priority'] == 'low' for todo in low_priority_todos)
    
    def test_get_stats(self):
        """Test getting todo statistics"""
        # Initially empty
        stats = self.todo_manager.get_stats()
        assert stats['total'] == 0
        assert stats['pending'] == 0
        assert stats['completed'] == 0
        assert stats['in_progress'] == 0
        assert stats['completion_rate'] == 0
        
        # Add todos with different statuses
        self.todo_manager.create_todo("Task 1", status="pending")
        self.todo_manager.create_todo("Task 2", status="completed")
        self.todo_manager.create_todo("Task 3", status="in_progress")
        self.todo_manager.create_todo("Task 4", status="completed")
        
        stats = self.todo_manager.get_stats()
        assert stats['total'] == 4
        assert stats['pending'] == 1
        assert stats['completed'] == 2
        assert stats['in_progress'] == 1
        assert stats['completion_rate'] == 50.0  # 2/4 * 100
    
    def test_get_overdue_todos(self):
        """Test getting overdue todos"""
        # Create todos with past due dates
        past_date = "2020-01-01"
        future_date = "2030-01-01"
        
        self.todo_manager.create_todo("Overdue task 1", due_date=past_date, status="pending")
        self.todo_manager.create_todo("Overdue task 2", due_date=past_date, status="in_progress")
        self.todo_manager.create_todo("Future task", due_date=future_date, status="pending")
        self.todo_manager.create_todo("Completed overdue", due_date=past_date, status="completed")
        
        overdue = self.todo_manager.get_overdue_todos()
        assert len(overdue) == 2  # Only pending and in_progress with past dates
        assert all(todo['due_date'] == past_date for todo in overdue)
        assert all(todo['status'] != 'completed' for todo in overdue)
    
    def test_persistence(self):
        """Test that todos are persisted to file"""
        # Create a todo
        todo = self.todo_manager.create_todo("Persistent task")
        
        # Create a new TodoManager instance (simulates app restart)
        new_manager = TodoManager(self.test_file)
        
        # Verify the todo is still there
        todos = new_manager.get_all_todos()
        assert len(todos) == 1
        assert todos[0]['title'] == "Persistent task"
        assert todos[0]['id'] == todo['id']
    
    def test_clear_all_todos(self):
        """Test clearing all todos"""
        # Add some todos
        self.todo_manager.create_todo("Task 1")
        self.todo_manager.create_todo("Task 2")
        assert len(self.todo_manager.get_all_todos()) == 2
        
        # Clear all todos
        self.todo_manager.clear_all_todos()
        assert len(self.todo_manager.get_all_todos()) == 0
