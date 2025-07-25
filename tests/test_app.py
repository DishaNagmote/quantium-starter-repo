import threading
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import sys
import os

# Import the Dash app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import app

# Start Dash app in a background thread
@pytest.fixture(scope="module", autouse=True)
def run_app():
    thread = threading.Thread(target=app.app.run, kwargs={"port": 8050})
    thread.daemon = True
    thread.start()
    time.sleep(3)
    yield

# Set up Selenium Chrome driver
@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    yield driver
    driver.quit()

def test_header_present(driver):
    driver.get("http://localhost:8050")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    header = driver.find_element(By.TAG_NAME, "h1")
    assert "Pink Morsel Sales Dashboard" in header.text

def test_graph_present(driver):
    driver.get("http://localhost:8050")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "sales-graph"))
    )
    graph = driver.find_element(By.ID, "sales-graph")
    assert graph is not None

def test_region_picker_present(driver):
    driver.get("http://localhost:8050")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "region-selector"))
    )
    dropdown = driver.find_element(By.ID, "region-selector")
    assert dropdown is not None
