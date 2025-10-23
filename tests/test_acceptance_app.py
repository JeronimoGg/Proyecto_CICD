import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from app.app import app
from app.todo_manager import TodoManager

BASE_URL = os.environ.get("APP_BASE_URL", "http://localhost:5000")

# Configuración del driver (Chrome headless)
@pytest.fixture
def browser():
    # Chrome (headless - sin interfaz gráfica)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Ejecuta sin interfaz gráfica
    options.add_argument("--no-sandbox") # Necesario para algunos entornos
    options.add_argument("--disable-dev-shm-usage") # Necesario para algunos entornos
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    
    yield driver
    driver.quit()

# Función de ayuda para limpiar datos de prueba
@pytest.fixture(autouse=True)
def cleanup_test_data():
    """Cleanup test data before and after each test"""
    test_file = "test_todos.json"
    
    # Set testing environment variable
    os.environ['TESTING'] = 'true'
    
    # Clear todos for each test (both test file and main file)
    todo_manager = TodoManager(test_file)
    todo_manager.clear_all_todos()
    
    # Also clear the main todos.json file
    main_todo_manager = TodoManager("todos.json")
    main_todo_manager.clear_all_todos()
    
    yield
    
    # Cleanup after test
    if 'TESTING' in os.environ:
        del os.environ['TESTING']
    
    # Clean up test file
    if os.path.exists(test_file):
        os.remove(test_file)
    
    # Also clean up main todos.json file
    main_todo_manager = TodoManager("todos.json")
    main_todo_manager.clear_all_todos()

def test_app_loads(browser):
    """Test that the application loads correctly"""
    # Navigate to the application
    browser.get(BASE_URL)
    
    # Wait for page to load (reduced timeout)
    WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )

    # Verify page title
    assert "To-Do List" in browser.title

    # Verify main heading exists
    heading = browser.find_element(By.TAG_NAME, "h1")
    assert "To-Do List" in heading.text

def test_add_simple_todo(browser):
    """Test adding a simple todo through the web interface"""
    # Navigate to the application
    browser.get(BASE_URL)
    
    # Wait for page to load
    WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.NAME, "title"))
    )

    # Count existing todos before adding
    existing_todos = browser.find_elements(By.CSS_SELECTOR, ".todo-item")
    initial_count = len(existing_todos)

    # Fill out only the required field (title)
    title_input = browser.find_element(By.NAME, "title")
    title_input.send_keys("Simple Test Task")

    # Submit the form
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()

    # Wait for page to reload and verify the todo was added
    WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".todo-item"))
    )

    # Verify the todo appears on the page (should be one more than before)
    todo_items = browser.find_elements(By.CSS_SELECTOR, ".todo-item")
    assert len(todo_items) == initial_count + 1

    # Verify the new todo has the correct title
    todo_titles = browser.find_elements(By.CSS_SELECTOR, ".todo-title")
    todo_texts = [title.text for title in todo_titles]
    assert "Simple Test Task" in todo_texts

def test_form_exists(browser):
    """Test that the form elements exist"""
    # Navigate to the application
    browser.get(BASE_URL)
    
    # Wait for page to load
    WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.NAME, "title"))
    )

    # Verify form elements exist
    browser.find_element(By.NAME, "title")
    browser.find_element(By.NAME, "description")
    browser.find_element(By.NAME, "priority")
    browser.find_element(By.NAME, "due_date")
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']")