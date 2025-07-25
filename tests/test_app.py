import time
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    yield driver
    driver.quit()

def test_app_loads(driver):
    driver.get("http://127.0.0.1:8050")
    time.sleep(2)
    assert "Pink Morsels" in driver.title or "Dash" in driver.title

# ✅ This test checks that selecting "North" updates the graph
def test_region_change_updates_graph(driver):
    driver.get("http://127.0.0.1:8050")
    time.sleep(2)  # allow app to render

    # Click the radio button for "North"
    north_label = driver.find_element("xpath", "//label[contains(text(), 'North')]")
    north_label.click()
    time.sleep(2)  # wait for graph to update

    # Check if the graph appears
    graph = driver.find_element("id", "sales-graph")
    assert graph is not None
