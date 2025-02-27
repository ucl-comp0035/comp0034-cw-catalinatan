from dash.testing.application_runners import import_app
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

def wait_for_element(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )

def test_dataset_button_and_offcanvas(dash_duo):
    """
    GIVEN the app is running
    WHEN the user hovers over and clicks the Dataset button
    THEN the tooltip should appear and the offcanvas should open
    """
    # Start the app in a server
    app = import_app(app_file="app")
    dash_duo.start_server(app)

    # Wait for and verify Dataset button
    data_attr_button = wait_for_element(dash_duo.driver, (By.ID, "data-attribution-button"))
    assert data_attr_button.text == "Dataset"

    # Hover over button and verify tooltip
    ActionChains(dash_duo.driver).move_to_element(data_attr_button).perform()
    dataset_tooltip = wait_for_element(dash_duo.driver, (By.ID, "dataset-tooltip"))
    assert dataset_tooltip.text == "View dataset attribution"

    # Open and verify offcanvas
    data_attr_button.click()
    data_attribution_canvas = wait_for_element(dash_duo.driver, (By.ID, "data-attribution-canvas"))
    assert data_attribution_canvas.is_displayed()

    # Verify offcanvas title
    offcanvas_title = wait_for_element(dash_duo.driver, (By.CLASS_NAME, "offcanvas-title"))
    assert offcanvas_title.text == "Dataset Attribution"

    # Verify offcanvas content
    canvas_text = data_attribution_canvas.text
    assert all(phrase in canvas_text for phrase in ["Greater London Authority", "Open Government Licence v2.0"])

    # Verify link in offcanvas
    link = data_attribution_canvas.find_element(By.TAG_NAME, "a")
    assert link.text == "this website"
    assert link.get_attribute("href") == "https://data.london.gov.uk/dataset/employment-occupation-type-and-gender-borough"
    assert link.get_attribute("target") == "_blank"

    # Close and verify offcanvas is closed
    ActionChains(dash_duo.driver).send_keys(Keys.ESCAPE).perform()
    try:
        WebDriverWait(dash_duo.driver, 10).until(
            EC.invisibility_of_element_located((By.ID, "data-attribution-canvas"))
        )
    except TimeoutException:
        pytest.fail("Offcanvas did not close within expected time")

