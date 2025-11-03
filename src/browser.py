"""Browser setup with Selenium"""
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.config import CHROME_VERSION, WINDOW_SIZE, TIMEOUT_ELEMENT

def create_undetected_driver(headless=False):
    """Create undetected Chrome driver"""
    options = uc.ChromeOptions()

    options.add_argument(f'--window-size={WINDOW_SIZE}')
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')

    if headless:
        options.add_argument('--headless=new')

    # Use Chrome version from config with keep_alive
    driver = uc.Chrome(
        options=options,
        version_main=CHROME_VERSION,
        use_subprocess=False,
        driver_executable_path=None
    )

    return driver

def wait_for_element(driver, selector, by=By.CSS_SELECTOR, timeout=None):
    """Wait for element to be present and return it"""
    if timeout is None:
        timeout = TIMEOUT_ELEMENT
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, selector))
        )
        return element
    except Exception:
        print(f"[WARN] Element not found: {selector}")
        return None

def wait_for_clickable(driver, selector, by=By.CSS_SELECTOR, timeout=None):
    """Wait for element to be clickable and return it"""
    if timeout is None:
        timeout = TIMEOUT_ELEMENT
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, selector))
        )
        return element
    except Exception:
        print(f"[WARN] Element not clickable: {selector}")
        return None
