"""
Pytest configuration and fixtures.
Handles setup/teardown logic for browser sessions with cross-browser support.
"""
import os
import shutil
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from config import Config


def pytest_addoption(parser):
    """Adds custom command line options for pytest."""
    parser.addoption(
        "--browser", 
        action="store", 
        default="chrome", 
        help="Browser to run tests: chrome or firefox"
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Stores test results in the node for access by fixtures (used for screenshots)."""
    outcome = yield
    rep = outcome.get_result()
    # Attach the report to the node so fixtures can access it
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function")
def browser(request):
    """
    Initializes a WebDriver instance based on the --browser option.
    Adds browser information to Allure reports and logs session info.
    """
    browser_name = request.config.getoption("--browser").lower()
    is_headless = os.getenv("CI") == "true" or Config.HEADLESS

    # Add Allure metadata
    allure.dynamic.parameter("browser", browser_name)
    allure.dynamic.label("browser", browser_name)
    allure.dynamic.tag(browser_name)

    driver = None
    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--disable-search-engine-choice-screen")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if is_headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=options)
        
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if is_headless:
            options.add_argument("-headless")
            options.add_argument("-width=1920")
            options.add_argument("-height=1080")
        driver = webdriver.Firefox(options=options)
        
    else:
        raise pytest.UsageError(f"--browser={browser_name} is not supported. Use 'chrome' or 'firefox'.")
    
    driver.maximize_window()
    
    yield driver
    
    # Capture screenshot on failure if the test failed during the execution phase
    if request.node.rep_call.failed if hasattr(request.node, 'rep_call') else False:
        try:
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"screenshot_{browser_name}_failure",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            # Fallback logging if screenshot fails
            print(f"Failed to capture screenshot: {e}")
    
    driver.quit()
    
    
def pytest_sessionfinish(session, exitstatus):
    """Generates the Allure report after the test session finishes."""
    # Prevent report generation on worker nodes when using pytest-xdist
    if hasattr(session.config, "workerinput"):
        return

    # Skip report generation in CI environments (handled by the workflow)
    if os.getenv("CI"):
        return

    if not shutil.which("npm"):
        print("\nNode.js not found. To enable report generation, please install Node.js & NPM from the official website: https://nodejs.org/en/download.")
        return

    if not os.path.isdir(os.path.join(str(session.config.rootdir), "node_modules")):
        print("\nNode.js dependencies not found. To enable report generation, please run 'npm ci' in the project root.")
        return

    os.system("npm run allure:awesome")
