import pytest
import warnings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    options = Options()

    # ✅ Headless mode with proper flags for Jenkins/Linux/macOS CI
    options.add_argument("--headless=new")  # For Chromium 109+
    options.add_argument("--no-sandbox")  # Required for CI (Linux)
    options.add_argument("--disable-dev-shm-usage")  # Prevent shared memory issues
    options.add_argument("--window-size=1920,1080")  # Optional: useful in headless

    # ✅ Create ChromeDriver using webdriver-manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()


def pytest_configure(config):
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=UserWarning)


def pytest_terminal_summary(terminalreporter, exitstatus):
    terminalreporter.write_sep("=", "🧪 TEST SUMMARY (TABLE FORMAT)")
    headers = f"{'Test Name':<40} {'Result':<10}"
    terminalreporter.write_line(headers)
    terminalreporter.write_line("-" * len(headers))

    for report in terminalreporter.stats.get('passed', []) + \
                  terminalreporter.stats.get('failed', []) + \
                  terminalreporter.stats.get('skipped', []):
        name = report.nodeid
        outcome = report.outcome.upper()
        terminalreporter.write_line(f"{name:<40} {outcome:<10}")