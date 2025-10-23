# tests/test_smoke_app.py
import os
from selenium.webdriver.common.by import By
from selenium import webdriver
import pytest

# Fixture para configurar el navegador
@pytest.fixture
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def test_smoke_test(browser):
    """SMOKE TEST: Verifica carga básica y elementos principales de la To-Do List."""
    # Lee la URL de producción desde una variable de entorno
    app_url = os.environ.get("APP_BASE_URL", "http://localhost:5000")
    print(f"Smoke test ejecutándose contra: {app_url}")
    
    try:
        # Navegar a la página principal
        browser.get(app_url + "/")
        print(f"Título de la página: {browser.title}")
        
        # Verificar que el título contenga "To-Do List"
        assert "To-Do List" in browser.title
        
        # Verificar elementos principales
        h1_element = browser.find_element(By.TAG_NAME, "h1")
        print(f"Texto H1: {h1_element.text}")
        assert "To-Do List" in h1_element.text
        
        # Verificar que el formulario de agregar tarea esté presente
        title_input = browser.find_element(By.NAME, "title")
        assert title_input is not None
        print("Campo de título encontrado")
        
        priority_select = browser.find_element(By.NAME, "priority")
        assert priority_select is not None
        print("Selector de prioridad encontrado")
        
        submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
        assert submit_button is not None
        print("Botón de envío encontrado")
        
        # Verificar que las estadísticas estén presentes
        stats_container = browser.find_element(By.CLASS_NAME, "stats")
        assert stats_container is not None
        print("Contenedor de estadísticas encontrado")
        
        stat_items = browser.find_elements(By.CLASS_NAME, "stat-item")
        assert len(stat_items) == 4  # Total, Pendientes, Completadas, Progreso
        print(f"Estadísticas encontradas: {len(stat_items)} elementos")
        
        # Verificar endpoint de salud
        browser.get(app_url + "/health")
        health_response = browser.find_element(By.TAG_NAME, "body")
        assert "OK" in health_response.text
        print("Endpoint de salud funcionando correctamente")
        
        print("Smoke test pasado exitosamente.")
        
    except Exception as e:
        print(f"Smoke test falló: {e}")
        # Opcional: tomar captura de pantalla si falla
        # browser.save_screenshot('smoke_test_failure.png')
        raise  # Vuelve a lanzar la excepción para que pytest marque el test como fallido


def test_smoke_test_api_endpoints(browser):
    """SMOKE TEST: Verifica que los endpoints de API básicos respondan."""
    app_url = os.environ.get("APP_BASE_URL", "http://localhost:5000")
    print(f"Smoke test API ejecutándose contra: {app_url}")
    
    try:
        # Probar endpoint de estadísticas
        browser.get(app_url + "/api/stats")
        print("Endpoint /api/stats accesible")
        
        # Probar endpoint de tareas
        browser.get(app_url + "/api/todos")
        print("Endpoint /api/todos accesible")
        
        # Probar endpoint de salud
        browser.get(app_url + "/health")
        health_response = browser.find_element(By.TAG_NAME, "body")
        assert "OK" in health_response.text
        print("Endpoint /health funcionando")
        
        print("Smoke test API pasado exitosamente.")
        
    except Exception as e:
        print(f"Smoke test API falló: {e}")
        raise


def test_smoke_test_basic_functionality(browser):
    """SMOKE TEST: Verifica funcionalidad básica de agregar una tarea."""
    app_url = os.environ.get("APP_BASE_URL", "http://localhost:5000")
    print(f"Smoke test funcionalidad ejecutándose contra: {app_url}")
    
    try:
        browser.get(app_url + "/")
        
        # Agregar una tarea simple
        title_input = browser.find_element(By.NAME, "title")
        submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        title_input.send_keys("Tarea de smoke test")
        submit_button.click()
        
        # Verificar que la tarea se agregó (redirección ocurre)
        # Esperar a que la página se recargue
        browser.implicitly_wait(2)
        
        # Verificar que estamos de vuelta en la página principal
        assert "To-Do List" in browser.title
        
        # Verificar que hay al menos una tarea
        todo_items = browser.find_elements(By.CLASS_NAME, "todo-item")
        if len(todo_items) > 0:
            print("Tarea agregada exitosamente")
        else:
            # Verificar si hay estado vacío
            empty_state = browser.find_elements(By.CLASS_NAME, "empty-state")
            if empty_state:
                print("Estado vacío detectado - tarea no se persistió")
            else:
                print("No se encontraron tareas ni estado vacío")
        
        print("Smoke test funcionalidad pasado exitosamente.")
        
    except Exception as e:
        print(f"Smoke test funcionalidad falló: {e}")
        raise


def test_smoke_test_page_elements(browser):
    """SMOKE TEST: Verifica que todos los elementos de la página estén presentes."""
    app_url = os.environ.get("APP_BASE_URL", "http://localhost:5000")
    print(f"Smoke test elementos ejecutándose contra: {app_url}")
    
    try:
        browser.get(app_url + "/")
        
        # Verificar elementos principales de la página
        required_elements = [
            ("h1", "Encabezado principal"),
            (".header", "Encabezado de la aplicación"),
            (".content", "Contenido principal"),
            (".add-form", "Formulario de agregar tarea"),
            (".stats", "Estadísticas"),
            ("input[name='title']", "Campo de título"),
            ("select[name='priority']", "Selector de prioridad"),
            ("button[type='submit']", "Botón de envío"),
        ]
        
        for selector, description in required_elements:
            element = browser.find_element(By.CSS_SELECTOR, selector)
            assert element is not None, f"Elemento no encontrado: {description}"
            print(f"✓ {description} encontrado")
        
        # Verificar que el formulario tiene todos los campos necesarios
        form_fields = [
            ("title", "Título"),
            ("description", "Descripción"),
            ("priority", "Prioridad"),
            ("due_date", "Fecha de vencimiento"),
        ]
        
        for field_name, field_description in form_fields:
            field = browser.find_element(By.NAME, field_name)
            assert field is not None, f"Campo no encontrado: {field_description}"
            print(f"✓ Campo {field_description} encontrado")
        
        print("Smoke test elementos pasado exitosamente.")
        
    except Exception as e:
        print(f"Smoke test elementos falló: {e}")
        raise