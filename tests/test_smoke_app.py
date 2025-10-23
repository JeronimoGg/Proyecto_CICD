import pytest
import requests
from app.app import app
from app.todo_manager import TodoManager


class TestSmokeApp:
    """Smoke tests for basic application functionality"""
    
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
        import os
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_application_starts(self):
        """Test that the application starts without errors"""
        response = self.app.get('/')
        assert response.status_code == 200
    
    def test_health_endpoint_responds(self):
        """Test that the health endpoint responds correctly"""
        response = self.app.get('/health')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert 'To-Do List App' in data['message']
    
    def test_main_page_contains_expected_elements(self):
        """Test that the main page contains expected elements"""
        response = self.app.get('/')
        assert response.status_code == 200
        
        # Check for key elements in the HTML
        html_content = response.get_data(as_text=True)
        assert 'To-Do List' in html_content
        assert 'Nueva Tarea' in html_content
        assert 'Mis Tareas' in html_content
        assert 'title' in html_content
        assert 'priority' in html_content
    
    def test_api_endpoints_respond(self):
        """Test that basic API endpoints respond"""
        # Test GET todos endpoint
        response = self.app.get('/api/todos')
        assert response.status_code == 200
        
        # Test stats endpoint
        response = self.app.get('/api/stats')
        assert response.status_code == 200
        
        # Test overdue todos endpoint
        response = self.app.get('/api/todos/overdue')
        assert response.status_code == 200
    
    def test_can_create_and_retrieve_todo(self):
        """Test basic CRUD functionality"""
        # Create a todo via API
        response = self.app.post('/api/todos',
                               json={
                                   'title': 'Smoke Test Task',
                                   'description': 'Testing basic functionality',
                                   'priority': 'medium'
                               })
        assert response.status_code == 201
        
        # Retrieve the todo
        data = response.get_json()
        todo_id = data['id']
        
        response = self.app.get(f'/api/todos/{todo_id}')
        assert response.status_code == 200
        
        retrieved_data = response.get_json()
        assert retrieved_data['title'] == 'Smoke Test Task'
        assert retrieved_data['id'] == todo_id
    
    def test_database_persistence(self):
        """Test that data persists between requests"""
        # Create a todo
        response = self.app.post('/api/todos',
                               json={
                                   'title': 'Persistence Test',
                                   'description': 'Testing data persistence'
                               })
        assert response.status_code == 201
        
        data = response.get_json()
        todo_id = data['id']
        
        # Verify the todo exists
        response = self.app.get(f'/api/todos/{todo_id}')
        assert response.status_code == 200
        
        # Create a new TodoManager instance (simulates app restart)
        todo_manager = TodoManager(self.test_file)
        todos = todo_manager.get_all_todos()
        
        assert len(todos) == 1
        assert todos[0]['title'] == 'Persistence Test'
        assert todos[0]['id'] == todo_id
    
    def test_error_handling(self):
        """Test that the application handles errors gracefully"""
        # Test getting non-existent todo
        response = self.app.get('/api/todos/999')
        assert response.status_code == 404
        
        # Test creating todo without title
        response = self.app.post('/api/todos',
                               json={
                                   'description': 'No title provided'
                               })
        assert response.status_code == 400
    
    def test_statistics_calculation(self):
        """Test that statistics are calculated correctly"""
        # Initially should have zero stats
        response = self.app.get('/api/stats')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['total'] == 0
        assert data['pending'] == 0
        assert data['completed'] == 0
        assert data['completion_rate'] == 0
        
        # Add some todos
        self.app.post('/api/todos', json={'title': 'Task 1'})
        self.app.post('/api/todos', json={'title': 'Task 2'})
        
        # Update one to completed
        todo_manager = TodoManager(self.test_file)
        todos = todo_manager.get_all_todos()
        todo_id = todos[0]['id']
        
        self.app.put(f'/api/todos/{todo_id}',
                    json={'status': 'completed'})
        
        # Check updated stats
        response = self.app.get('/api/stats')
        data = response.get_json()
        
        assert data['total'] == 2
        assert data['pending'] == 1
        assert data['completed'] == 1
        assert data['completion_rate'] == 50.0
