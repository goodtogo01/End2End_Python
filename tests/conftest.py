import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    options = Options()
    # options.add_argument("--headless=new")  # Optional: Headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


def pytest_configure(config):
    import warnings
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
