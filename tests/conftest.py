import os
import pytest
from selenium.webdriver.chrome.options import Options
from dash.testing.application_runners import import_app
import src.app as app
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dash import no_update
from dash.exceptions import PreventUpdate
from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict
from dash.testing.composite import DashComposite

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

@pytest.fixture()
def start_dash_app(dash_duo):
    dash_app = import_app(app_file="app")
    dash_duo.start_server(dash_app)
    return dash_duo

@pytest.fixture()
def dash_driver(dash_duo):
    return dash_duo.driver

@pytest.fixture()
def wait_for_visible_element():
    def _wait_for_visible_element(driver, locator, timeout=10):
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    return _wait_for_visible_element

@pytest.fixture()
def wait_for_clickable_element():
    def _wait_for_clickable_element(driver, locator, timeout=10):
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
    return _wait_for_clickable_element

