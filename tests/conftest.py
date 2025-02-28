import os
import pytest
from selenium.webdriver.chrome.options import Options
from dash.testing.application_runners import import_app
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def chrome_options():
    """
    Configure Chrome options for pytest.

    Returns
    -------
    Options
        Configured Chrome options.
    """
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
    """
    Start the Dash app for testing.

    Parameters
    ----------
    dash_duo : DashDuo
        The Dash testing fixture.

    Returns
    -------
    DashDuo
        The Dash testing fixture with the app started.
    """
    dash_app = import_app(app_file="app")
    dash_duo.start_server(dash_app)
    return dash_duo


@pytest.fixture()
def dash_driver(dash_duo):
    """
    Get the Selenium WebDriver for the Dash app.

    Parameters
    ----------
    dash_duo : DashDuo
        The Dash testing fixture.

    Returns
    -------
    WebDriver
        The Selenium WebDriver for the Dash app.
    """
    return dash_duo.driver


@pytest.fixture()
def wait_for_visible_element():
    """
    Wait for an element to be visible.

    Returns
    -------
    function
        A function that waits for an element to be visible.
    """
    def _wait_for_visible_element(driver, locator, timeout=10):
        """
        Wait for an element to be visible.

        Parameters
        ----------
        driver : WebDriver
            The Selenium WebDriver.
        locator : tuple
            The locator for the element.
        timeout : int, optional
            The timeout in seconds, by default 10.

        Returns
        -------
        WebElement
            The visible WebElement.
        """
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    return _wait_for_visible_element


@pytest.fixture()
def wait_for_clickable_element():
    """
    Wait for an element to be clickable.

    Returns
    -------
    function
        A function that waits for an element to be clickable.
    """
    def _wait_for_clickable_element(driver, locator, timeout=10):
        """
        Wait for an element to be clickable.

        Parameters
        ----------
        driver : WebDriver
            The Selenium WebDriver.
        locator : tuple
            The locator for the element.
        timeout : int, optional
            The timeout in seconds, by default 10.

        Returns
        -------
        WebElement
            The clickable WebElement.
        """
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
    return _wait_for_clickable_element
