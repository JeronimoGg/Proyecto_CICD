import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta

BASE_URL = os.environ.get("APP_BASE_URL", "http://localhost:5000")

# Configuración del driver
@pytest.fixture
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def wait_for_element(browser, by, value, timeout=10):
    """Espera a que un elemento sea visible"""
    try:
        element = WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        return None


def get_todo_items(browser):
    """Obtiene todos los elementos de tareas"""
    return browser.find_elements(By.CLASS_NAME, "todo-item")


def test_todo_list_page_loads(browser):
    """Prueba que la página de To-Do List carga correctamente"""
    browser.get(BASE_URL)
    
    # Verificar elementos principales
    assert "To-Do List" in browser.title
    assert wait_for_element(browser, By.TAG_NAME, "h1") is not None
    
    h1 = browser.find_element(By.TAG_NAME, "h1")
    assert "To-Do List" in h1.text
    
    # Verificar formulario de agregar tarea
    assert wait_for_element(browser, By.NAME, "title") is not None
    assert wait_for_element(browser, By.NAME, "priority") is not None
    assert wait_for_element(browser, By.CSS_SELECTOR, "button[type='submit']") is not None


def test_add_todo_success(browser):
    """Prueba agregar una tarea exitosamente"""
    browser.get(BASE_URL)
    
    # Llenar el formulario
    title_input = browser.find_element(By.NAME, "title")
    description_input = browser.find_element(By.NAME, "description")
    priority_select = Select(browser.find_element(By.NAME, "priority"))
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    
    title_input.send_keys("Tarea de prueba")
    description_input.send_keys("Esta es una descripción de prueba")
    priority_select.select_by_value("alta")
    submit_button.click()
    
    # Verificar que la tarea se agregó
    wait_for_element(browser, By.CLASS_NAME, "todo-item")
    todo_items = get_todo_items(browser)
    assert len(todo_items) == 1
    
    # Verificar contenido de la tarea
    todo_title = browser.find_element(By.CLASS_NAME, "todo-title")
    assert "Tarea de prueba" in todo_title.text
    
    todo_description = browser.find_element(By.CLASS_NAME, "todo-description")
    assert "Esta es una descripción de prueba" in todo_description.text
    
    todo_priority = browser.find_element(By.CLASS_NAME, "priority-alta")
    assert "alta" in todo_priority.text


def test_add_todo_empty_title(browser):
    """Prueba agregar una tarea con título vacío"""
    browser.get(BASE_URL)
    
    # Intentar enviar formulario vacío
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()
    
    # Verificar que no se agregó ninguna tarea
    todo_items = get_todo_items(browser)
    assert len(todo_items) == 0


def test_complete_todo(browser):
    """Prueba marcar una tarea como completada"""
    browser.get(BASE_URL)
    
    # Agregar una tarea
    title_input = browser.find_element(By.NAME, "title")
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    
    title_input.send_keys("Tarea para completar")
    submit_button.click()
    
    # Esperar a que aparezca la tarea
    wait_for_element(browser, By.CLASS_NAME, "todo-item")
    
    # Marcar como completada
    complete_button = browser.find_element(By.CSS_SELECTOR, ".btn-success")
    complete_button.click()
    
    # Verificar que la tarea se marcó como completada
    todo_item = browser.find_element(By.CLASS_NAME, "todo-item")
    assert "completed" in todo_item.get_attribute("class")
    
    # Verificar que el botón cambió a "Reabrir"
    reopen_button = browser.find_element(By.CSS_SELECTOR, ".btn-secondary")
    assert "Reabrir" in reopen_button.text


def test_reopen_todo(browser):
    """Prueba reabrir una tarea completada"""
    browser.get(BASE_URL)
    
    # Agregar y completar una tarea
    title_input = browser.find_element(By.NAME, "title")
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    
    title_input.send_keys("Tarea para reabrir")
    submit_button.click()
    
    wait_for_element(browser, By.CLASS_NAME, "todo-item")
    
    # Completar
    complete_button = browser.find_element(By.CSS_SELECTOR, ".btn-success")
    complete_button.click()
    
    # Reabrir
    reopen_button = browser.find_element(By.CSS_SELECTOR, ".btn-secondary")
    reopen_button.click()
    
    # Verificar que la tarea se reabrió
    todo_item = browser.find_element(By.CLASS_NAME, "todo-item")
    assert "completed" not in todo_item.get_attribute("class")
    
    # Verificar que el botón cambió de vuelta a "Completar"
    complete_button = browser.find_element(By.CSS_SELECTOR, ".btn-success")
    assert "Completar" in complete_button.text


def test_delete_todo(browser):
    """Prueba eliminar una tarea"""
    browser.get(BASE_URL)
    
    # Agregar una tarea
    title_input = browser.find_element(By.NAME, "title")
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    
    title_input.send_keys("Tarea para eliminar")
    submit_button.click()
    
    wait_for_element(browser, By.CLASS_NAME, "todo-item")
    
    # Eliminar la tarea
    delete_button = browser.find_element(By.CSS_SELECTOR, ".btn-danger")
    delete_button.click()
    
    # Confirmar eliminación en el diálogo
    browser.switch_to.alert.accept()
    
    # Verificar que la tarea se eliminó
    todo_items = get_todo_items(browser)
    assert len(todo_items) == 0


def test_multiple_todos(browser):
    """Prueba agregar múltiples tareas"""
    browser.get(BASE_URL)
    
    # Agregar primera tarea
    title_input = browser.find_element(By.NAME, "title")
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    
    title_input.send_keys("Primera tarea")
    submit_button.click()
    
    wait_for_element(browser, By.CLASS_NAME, "todo-item")
    
    # Agregar segunda tarea
    title_input.clear()
    title_input.send_keys("Segunda tarea")
    submit_button.click()
    
    # Verificar que hay dos tareas
    todo_items = get_todo_items(browser)
    assert len(todo_items) == 2
    
    # Verificar contenido
    todo_titles = browser.find_elements(By.CLASS_NAME, "todo-title")
    assert "Primera tarea" in todo_titles[0].text
    assert "Segunda tarea" in todo_titles[1].text


def test_priority_levels(browser):
    """Prueba diferentes niveles de prioridad"""
    browser.get(BASE_URL)
    
    priorities = ["baja", "media", "alta"]
    priority_classes = ["priority-baja", "priority-media", "priority-alta"]
    
    for i, priority in enumerate(priorities):
        # Agregar tarea con prioridad específica
        title_input = browser.find_element(By.NAME, "title")
        priority_select = Select(browser.find_element(By.NAME, "priority"))
        submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        title_input.send_keys(f"Tarea {priority}")
        priority_select.select_by_value(priority)
        submit_button.click()
        
        wait_for_element(browser, By.CLASS_NAME, "todo-item")
    
    # Verificar que todas las tareas tienen la prioridad correcta
    todo_items = get_todo_items(browser)
    assert len(todo_items) == 3
    
    for i, item in enumerate(todo_items):
        priority_element = item.find_element(By.CLASS_NAME, priority_classes[i])
        assert priority_element is not None


def test_due_date(browser):
    """Prueba agregar una tarea con fecha de vencimiento"""
    browser.get(BASE_URL)
    
    # Calcular fecha futura
    future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    
    # Llenar formulario con fecha de vencimiento
    title_input = browser.find_element(By.NAME, "title")
    due_date_input = browser.find_element(By.NAME, "due_date")
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    
    title_input.send_keys("Tarea con fecha")
    due_date_input.send_keys(future_date)
    submit_button.click()
    
    wait_for_element(browser, By.CLASS_NAME, "todo-item")
    
    # Verificar que la fecha se muestra
    todo_meta = browser.find_element(By.CLASS_NAME, "todo-meta")
    assert future_date in todo_meta.text


def test_stats_display(browser):
    """Prueba que las estadísticas se muestren correctamente"""
    browser.get(BASE_URL)
    
    # Verificar elementos de estadísticas
    stats_container = browser.find_element(By.CLASS_NAME, "stats")
    assert stats_container is not None
    
    stat_items = browser.find_elements(By.CLASS_NAME, "stat-item")
    assert len(stat_items) == 4  # Total, Pendientes, Completadas, Progreso
    
    # Verificar que los números iniciales son 0
    stat_numbers = browser.find_elements(By.CLASS_NAME, "stat-number")
    assert "0" in stat_numbers[0].text  # Total
    assert "0" in stat_numbers[1].text  # Pendientes
    assert "0" in stat_numbers[2].text  # Completadas
    assert "0" in stat_numbers[3].text  # Progreso


def test_stats_update_after_todo_creation(browser):
    """Prueba que las estadísticas se actualicen al crear una tarea"""
    browser.get(BASE_URL)
    
    # Obtener estadísticas iniciales
    stat_numbers = browser.find_elements(By.CLASS_NAME, "stat-number")
    initial_total = int(stat_numbers[0].text)
    
    # Agregar una tarea
    title_input = browser.find_element(By.NAME, "title")
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    
    title_input.send_keys("Tarea para estadísticas")
    submit_button.click()
    
    wait_for_element(browser, By.CLASS_NAME, "todo-item")
    
    # Verificar que las estadísticas se actualizaron
    stat_numbers = browser.find_elements(By.CLASS_NAME, "stat-number")
    assert int(stat_numbers[0].text) == initial_total + 1  # Total
    assert int(stat_numbers[1].text) == initial_total + 1  # Pendientes


def test_empty_state(browser):
    """Prueba el estado vacío cuando no hay tareas"""
    browser.get(BASE_URL)
    
    # Verificar que se muestra el estado vacío
    empty_state = browser.find_element(By.CLASS_NAME, "empty-state")
    assert empty_state is not None
    
    empty_title = empty_state.find_element(By.TAG_NAME, "h3")
    assert "No hay tareas" in empty_title.text or "¡No hay tareas!" in empty_title.text


def test_responsive_design(browser):
    """Prueba que el diseño sea responsive"""
    browser.get(BASE_URL)
    
    # Verificar que los elementos principales están presentes
    assert browser.find_element(By.CLASS_NAME, "container") is not None
    assert browser.find_element(By.CLASS_NAME, "header") is not None
    assert browser.find_element(By.CLASS_NAME, "content") is not None
    
    # Verificar que el formulario tiene la estructura correcta
    form_row = browser.find_element(By.CLASS_NAME, "form-row")
    assert form_row is not None


@pytest.mark.parametrize(
    "title, description, priority, expected_result",
    [
        ("Tarea simple", "", "media", True),
        ("Tarea con descripción", "Descripción detallada", "alta", True),
        ("Tarea baja prioridad", "Descripción", "baja", True),
        ("", "Solo descripción", "media", False),  # Título vacío
    ],
)
def test_todo_creation_scenarios(browser, title, description, priority, expected_result):
    """Prueba diferentes escenarios de creación de tareas"""
    browser.get(BASE_URL)
    
    # Llenar formulario
    title_input = browser.find_element(By.NAME, "title")
    description_input = browser.find_element(By.NAME, "description")
    priority_select = Select(browser.find_element(By.NAME, "priority"))
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    
    title_input.send_keys(title)
    description_input.send_keys(description)
    priority_select.select_by_value(priority)
    submit_button.click()
    
    if expected_result:
        # Verificar que la tarea se creó
        wait_for_element(browser, By.CLASS_NAME, "todo-item")
        todo_items = get_todo_items(browser)
        assert len(todo_items) >= 1
    else:
        # Verificar que no se creó la tarea
        todo_items = get_todo_items(browser)
        assert len(todo_items) == 0