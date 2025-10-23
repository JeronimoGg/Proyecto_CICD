import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from app.app import app
from app.todo_manager import TodoManager


class TestAcceptanceApp:
    """Acceptance tests for To-Do List application using Selenium"""
    
    def setup_method(self):
        """Setup method run before each test"""
        self.test_file = "test_todos.json"
        
        # Set testing environment variable
        os.environ['TESTING'] = 'true'
        
        # Clear todos for each test
        todo_manager = TodoManager(self.test_file)
        todo_manager.clear_all_todos()
        
        # Setup Selenium WebDriver
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        
        # Start Flask app in test mode
        self.app = app.test_client()
        self.app.testing = True
    
    def teardown_method(self):
        """Cleanup method run after each test"""
        self.driver.quit()
        
        # Clear testing environment variable
        if 'TESTING' in os.environ:
            del os.environ['TESTING']
        
        # Clean up test file
        import os
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_add_todo_through_ui(self):
        """Test adding a todo through the web interface"""
        # Navigate to the application
        self.driver.get("http://localhost:5000")
        
        # Wait for page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        
        # Verify page title
        assert "To-Do List" in self.driver.title
        
        # Fill out the form
        title_input = self.driver.find_element(By.NAME, "title")
        title_input.send_keys("Test Task from UI")
        
        description_input = self.driver.find_element(By.NAME, "description")
        description_input.send_keys("This is a test description")
        
        priority_select = Select(self.driver.find_element(By.NAME, "priority"))
        priority_select.select_by_value("high")
        
        due_date_input = self.driver.find_element(By.NAME, "due_date")
        due_date_input.send_keys("2024-12-31")
        
        # Submit the form
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Wait for page to reload and verify the todo was added
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".todo-item"))
        )
        
        # Verify the todo appears on the page
        todo_items = self.driver.find_elements(By.CSS_SELECTOR, ".todo-item")
        assert len(todo_items) == 1
        
        todo_title = self.driver.find_element(By.CSS_SELECTOR, ".todo-title")
        assert "Test Task from UI" in todo_title.text
        
        # Verify priority is displayed correctly
        priority_badge = self.driver.find_element(By.CSS_SELECTOR, ".priority-high")
        assert "high" in priority_badge.text.lower()
    
    def test_complete_todo_through_ui(self):
        """Test completing a todo through the web interface"""
        # First add a todo
        self.driver.get("http://localhost:5000")
        
        # Add a todo
        title_input = self.driver.find_element(By.NAME, "title")
        title_input.send_keys("Task to Complete")
        
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Wait for the todo to appear
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".todo-item"))
        )
        
        # Find and click the complete button
        complete_button = self.driver.find_element(By.CSS_SELECTOR, ".btn-success")
        complete_button.click()
        
        # Wait for page to reload
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".todo-item.completed"))
        )
        
        # Verify the todo is marked as completed
        completed_todo = self.driver.find_element(By.CSS_SELECTOR, ".todo-item.completed")
        assert completed_todo is not None
        
        # Verify the status badge shows completed
        status_badge = completed_todo.find_element(By.CSS_SELECTOR, ".status-completed")
        assert "completada" in status_badge.text.lower()
    
    def test_delete_todo_through_ui(self):
        """Test deleting a todo through the web interface"""
        # First add a todo
        self.driver.get("http://localhost:5000")
        
        # Add a todo
        title_input = self.driver.find_element(By.NAME, "title")
        title_input.send_keys("Task to Delete")
        
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Wait for the todo to appear
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".todo-item"))
        )
        
        # Verify the todo exists
        todo_items = self.driver.find_elements(By.CSS_SELECTOR, ".todo-item")
        assert len(todo_items) == 1
        
        # Find and click the delete button
        delete_button = self.driver.find_element(By.CSS_SELECTOR, ".btn-danger")
        delete_button.click()
        
        # Handle the confirmation dialog
        self.driver.switch_to.alert.accept()
        
        # Wait for page to reload and verify the todo was deleted
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".empty-state"))
        )
        
        # Verify the empty state message appears
        empty_state = self.driver.find_element(By.CSS_SELECTOR, ".empty-state")
        assert "No hay tareas pendientes" in empty_state.text
    
    def test_multiple_todos_management(self):
        """Test managing multiple todos through the UI"""
        self.driver.get("http://localhost:5000")
        
        # Add multiple todos
        todos_to_add = [
            ("High Priority Task", "high"),
            ("Medium Priority Task", "medium"),
            ("Low Priority Task", "low")
        ]
        
        for title, priority in todos_to_add:
            title_input = self.driver.find_element(By.NAME, "title")
            title_input.clear()
            title_input.send_keys(title)
            
            priority_select = Select(self.driver.find_element(By.NAME, "priority"))
            priority_select.select_by_value(priority)
            
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            
            # Wait for the todo to appear
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".todo-item"))
            )
        
        # Verify all todos are displayed
        todo_items = self.driver.find_elements(By.CSS_SELECTOR, ".todo-item")
        assert len(todo_items) == 3
        
        # Verify statistics are updated
        stats_numbers = self.driver.find_elements(By.CSS_SELECTOR, ".stat-number")
        assert len(stats_numbers) == 4  # total, pending, completed, progress
        
        total_stat = stats_numbers[0]
        assert total_stat.text == "3"
        
        pending_stat = stats_numbers[1]
        assert pending_stat.text == "3"
    
    def test_form_validation(self):
        """Test form validation for empty title"""
        self.driver.get("http://localhost:5000")
        
        # Try to submit form with empty title
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # The form should not submit (HTML5 validation)
        # Verify no todos were added
        todo_items = self.driver.find_elements(By.CSS_SELECTOR, ".todo-item")
        assert len(todo_items) == 0
    
    def test_responsive_design(self):
        """Test that the application is responsive"""
        self.driver.get("http://localhost:5000")
        
        # Test desktop view
        self.driver.set_window_size(1200, 800)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".container"))
        )
        
        # Verify desktop layout
        container = self.driver.find_element(By.CSS_SELECTOR, ".container")
        assert container.is_displayed()
        
        # Test mobile view
        self.driver.set_window_size(375, 667)  # iPhone size
        
        # Verify mobile layout still works
        container = self.driver.find_element(By.CSS_SELECTOR, ".container")
        assert container.is_displayed()
        
        # Verify form is still usable on mobile
        title_input = self.driver.find_element(By.NAME, "title")
        assert title_input.is_displayed()
        
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        assert submit_button.is_displayed()
