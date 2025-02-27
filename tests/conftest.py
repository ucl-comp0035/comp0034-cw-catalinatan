import os
import pytest
from selenium.webdriver.chrome.options import Options
from dash.testing.application_runners import import_app
import src.app as app
from dash import no_update
from dash.exceptions import PreventUpdate
from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict

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

@pytest.fixture(autouse=True)
def start_app(dash_duo):
    """ Pytest fixture to start the Dash app in a threaded server.
    This is a function-scoped fixture.
    Automatically used by all tests in this module.
    """
    app_file_loc = "app"
    app = import_app(app_file_loc)
    yield dash_duo.start_server(app)


@pytest.fixture()
def app_url(start_app, dash_duo):
    """ Pytest fixture for the URL of the running Dash app. """
    yield dash_duo.server_url


@pytest.fixture()
def dash_app():
    return app