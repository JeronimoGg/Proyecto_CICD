import pytest
import json
import os
from app.app import app
from app.todo_manager import TodoManager


class TestAppIntegration:
    """Integration tests for Flask application"""
    
    def setup_method(self):
        """Setup method run before each test"""
        self.test_file = "test_todos.json"
        self.app = app.test_client()
        self.app.testing = True
        
        # Clear todos for each test
        todo_manager = TodoManager(self.test_file)
        todo_manager.clear_all_todos()
    
    def teardown_method(self):
        """Cleanup method run after each test"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_index_page_loads(self):
        """Test that the index page loads successfully"""
        response = self.app.get('/')
        assert response.status_code == 200
        assert b'To-Do List' in response.data
        assert b'Nueva Tarea' in response.data
    
    def test_add_todo_form_submission(self):
        """Test adding a todo via form submission"""
        response = self.app.post('/add', data={
            'title': 'Test Task',
            'description': 'Test Description',
            'priority': 'high',
            'due_date': '2024-12-31'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Test Task' in response.data
    
    def test_add_todo_empty_title(self):
        """Test adding a todo with empty title"""
        response = self.app.post('/add', data={
            'title': '',
            'description': 'Test Description'
        })
        
        assert response.status_code == 400
    
    def test_update_todo_status(self):
        """Test updating todo status"""
        # First add a todo
        self.app.post('/add', data={
            'title': 'Test Task',
            'description': 'Test Description'
        })
        
        # Get the todo ID (assuming it's 1)
        todo_manager = TodoManager(self.test_file)
        todos = todo_manager.get_all_todos()
        todo_id = todos[0]['id']
        
        # Update status to completed
        response = self.app.post(f'/update/{todo_id}', data={
            'status': 'completed'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        
        # Verify the todo was updated
        updated_todo = todo_manager.get_todo_by_id(todo_id)
        assert updated_todo['status'] == 'completed'
    
    def test_delete_todo(self):
        """Test deleting a todo"""
        # First add a todo
        self.app.post('/add', data={
            'title': 'Test Task',
            'description': 'Test Description'
        })
        
        # Get the todo ID
        todo_manager = TodoManager(self.test_file)
        todos = todo_manager.get_all_todos()
        todo_id = todos[0]['id']
        
        # Delete the todo
        response = self.app.post(f'/delete/{todo_id}', follow_redirects=True)
        
        assert response.status_code == 200
        
        # Verify the todo was deleted
        assert len(todo_manager.get_all_todos()) == 0
    
    def test_api_get_todos(self):
        """Test API endpoint to get all todos"""
        # Add some todos
        todo_manager = TodoManager(self.test_file)
        todo_manager.create_todo("Task 1")
        todo_manager.create_todo("Task 2")
        
        response = self.app.get('/api/todos')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data) == 2
        assert data[0]['title'] == "Task 1"
        assert data[1]['title'] == "Task 2"
    
    def test_api_get_todo_by_id(self):
        """Test API endpoint to get a specific todo"""
        # Add a todo
        todo_manager = TodoManager(self.test_file)
        todo = todo_manager.create_todo("Test Task")
        todo_id = todo['id']
        
        response = self.app.get(f'/api/todos/{todo_id}')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['title'] == "Test Task"
        assert data['id'] == todo_id
    
    def test_api_get_todo_by_id_not_found(self):
        """Test API endpoint to get non-existent todo"""
        response = self.app.get('/api/todos/999')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_api_create_todo(self):
        """Test API endpoint to create a todo"""
        response = self.app.post('/api/todos', 
                               data=json.dumps({
                                   'title': 'API Task',
                                   'description': 'API Description',
                                   'priority': 'high',
                                   'due_date': '2024-12-31'
                               }),
                               content_type='application/json')
        
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['title'] == 'API Task'
        assert data['description'] == 'API Description'
        assert data['priority'] == 'high'
        assert data['due_date'] == '2024-12-31'
    
    def test_api_create_todo_missing_title(self):
        """Test API endpoint to create todo without title"""
        response = self.app.post('/api/todos',
                               data=json.dumps({
                                   'description': 'API Description'
                               }),
                               content_type='application/json')
        
        assert response.status_code == 400
        
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_api_update_todo(self):
        """Test API endpoint to update a todo"""
        # First create a todo
        todo_manager = TodoManager(self.test_file)
        todo = todo_manager.create_todo("Original Task")
        todo_id = todo['id']
        
        # Update the todo
        response = self.app.put(f'/api/todos/{todo_id}',
                              data=json.dumps({
                                  'title': 'Updated Task',
                                  'status': 'completed',
                                  'priority': 'high'
                              }),
                              content_type='application/json')
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['title'] == 'Updated Task'
        assert data['status'] == 'completed'
        assert data['priority'] == 'high'
    
    def test_api_update_todo_not_found(self):
        """Test API endpoint to update non-existent todo"""
        response = self.app.put('/api/todos/999',
                              data=json.dumps({
                                  'title': 'Updated Task'
                              }),
                              content_type='application/json')
        
        assert response.status_code == 404
    
    def test_api_delete_todo(self):
        """Test API endpoint to delete a todo"""
        # First create a todo
        todo_manager = TodoManager(self.test_file)
        todo = todo_manager.create_todo("Test Task")
        todo_id = todo['id']
        
        # Delete the todo
        response = self.app.delete(f'/api/todos/{todo_id}')
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'message' in data
        
        # Verify the todo was deleted
        assert todo_manager.get_todo_by_id(todo_id) is None
    
    def test_api_delete_todo_not_found(self):
        """Test API endpoint to delete non-existent todo"""
        response = self.app.delete('/api/todos/999')
        assert response.status_code == 404
    
    def test_api_get_todos_by_status(self):
        """Test API endpoint to get todos by status"""
        # Add todos with different statuses
        todo_manager = TodoManager(self.test_file)
        todo_manager.create_todo("Task 1", status="pending")
        todo_manager.create_todo("Task 2", status="completed")
        
        response = self.app.get('/api/todos/status/pending')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['title'] == "Task 1"
        assert data[0]['status'] == "pending"
    
    def test_api_get_todos_by_priority(self):
        """Test API endpoint to get todos by priority"""
        # Add todos with different priorities
        todo_manager = TodoManager(self.test_file)
        todo_manager.create_todo("Task 1", priority="high")
        todo_manager.create_todo("Task 2", priority="low")
        
        response = self.app.get('/api/todos/priority/high')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['title'] == "Task 1"
        assert data[0]['priority'] == "high"
    
    def test_api_get_stats(self):
        """Test API endpoint to get statistics"""
        # Add todos with different statuses
        todo_manager = TodoManager(self.test_file)
        todo_manager.create_todo("Task 1", status="pending")
        todo_manager.create_todo("Task 2", status="completed")
        todo_manager.create_todo("Task 3", status="in_progress")
        
        response = self.app.get('/api/stats')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['total'] == 3
        assert data['pending'] == 1
        assert data['completed'] == 1
        assert data['in_progress'] == 1
        assert data['completion_rate'] == 33.33
    
    def test_api_get_overdue_todos(self):
        """Test API endpoint to get overdue todos"""
        # Add todos with past due dates
        todo_manager = TodoManager(self.test_file)
        todo_manager.create_todo("Overdue Task", due_date="2020-01-01", status="pending")
        todo_manager.create_todo("Future Task", due_date="2030-01-01", status="pending")
        
        response = self.app.get('/api/todos/overdue')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['title'] == "Overdue Task"
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.app.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'To-Do List App' in data['message']
