import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from app.app import app
from app.todo_manager import TodoManager


class TestAcceptanceApp:
    """Simplified acceptance tests for To-Do List application using Selenium"""
    
    def setup_method(self):
        """Setup method run before each test"""
        self.test_file = "test_todos.json"
        
        # Set testing environment variable
        os.environ['TESTING'] = 'true'
        
        # Clear todos for each test (both test file and main file)
        todo_manager = TodoManager(self.test_file)
        todo_manager.clear_all_todos()
        
        # Also clear the main todos.json file
        main_todo_manager = TodoManager("todos.json")
        main_todo_manager.clear_all_todos()
        
        # Setup Chrome WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run in background
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)  # Reduced wait time
    
    def teardown_method(self):
        """Cleanup method run after each test"""
        if hasattr(self, 'driver'):
            self.driver.quit()
        
        # Clear testing environment variable
        if 'TESTING' in os.environ:
            del os.environ['TESTING']
        
        # Clean up test file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        
        # Also clean up main todos.json file
        main_todo_manager = TodoManager("todos.json")
        main_todo_manager.clear_all_todos()
    
    def test_app_loads(self):
        """Test that the application loads correctly"""
        # Navigate to the application
        self.driver.get("http://localhost:5000")
        
        # Wait for page to load (reduced timeout)
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        
        # Verify page title
        assert "To-Do List" in self.driver.title
        
        # Verify main heading exists
        heading = self.driver.find_element(By.TAG_NAME, "h1")
        assert "To-Do List" in heading.text
    
    def test_add_simple_todo(self):
        """Test adding a simple todo through the web interface"""
        # Navigate to the application
        self.driver.get("http://localhost:5000")
        
        # Wait for page to load
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.NAME, "title"))
        )
        
        # Count existing todos before adding
        existing_todos = self.driver.find_elements(By.CSS_SELECTOR, ".todo-item")
        initial_count = len(existing_todos)
        
        # Fill out only the required field (title)
        title_input = self.driver.find_element(By.NAME, "title")
        title_input.send_keys("Simple Test Task")
        
        # Submit the form
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Wait for page to reload and verify the todo was added
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".todo-item"))
        )
        
        # Verify the todo appears on the page (should be one more than before)
        todo_items = self.driver.find_elements(By.CSS_SELECTOR, ".todo-item")
        assert len(todo_items) == initial_count + 1
        
        # Verify the new todo has the correct title
        todo_titles = self.driver.find_elements(By.CSS_SELECTOR, ".todo-title")
        todo_texts = [title.text for title in todo_titles]
        assert "Simple Test Task" in todo_texts
    
    def test_form_exists(self):
        """Test that the form elements exist"""
        # Navigate to the application
        self.driver.get("http://localhost:5000")
        
        # Wait for page to load
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.NAME, "title"))
        )
        
        # Verify form elements exist
        assert self.driver.find_element(By.NAME, "title")
        assert self.driver.find_element(By.NAME, "description")
        assert self.driver.find_element(By.NAME, "priority")
        assert self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")