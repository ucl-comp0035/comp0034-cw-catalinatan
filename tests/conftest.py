import os
import pytest
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def chrome_options():
    """Configure Chrome options for pytest"""
    options = Options()
    if "GITHUB_ACTIONS" in os.environ:
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
    else:
        options.add_argument("start-maximized")
    return options