from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def test_region_and_year_dropdown(start_dash_app, dash_duo,
                                  dash_driver, wait_for_visible_element,
                                  wait_for_clickable_element):
    """
    GIVEN the app is running
    WHEN the user selects a region and year
    THEN the region and year dropdowns should update
    AND charts should be displayed
    AND the user should be able to clear the year selection
    """
    # Locate the region dropdown and verify its placeholder text
    region_dropdown = wait_for_clickable_element(dash_driver,
                                                 (By.ID, "region-dropdown"))
    region_placeholder = region_dropdown.find_element(By.CSS_SELECTOR,
                                                      ".Select-placeholder"
                                                      ).text
    assert region_placeholder == "Select a region"

    # Define chart card IDs and their body IDs
    chart_card_ids = ['bar-chart-card', 'pie-chart-card', 'disparity-map-card',
                      'stacked-area-chart-card']
    chart_card_body_ids = ['bar-chart-card-body', 'pie-chart-card-body',
                           'disparity-map-card-body',
                           'stacked-area-chart-card-body']
    custom_placeholder_class = "custom-placeholder"
    icon_placeholder_css = "i.custom-icon.bi.bi-lock"

    # Verify that each chart card and its body are displayed with placeholders
    for chart_card_id, chart_card_body_id in zip(chart_card_ids,
                                                 chart_card_body_ids):
        chart_card = wait_for_visible_element(dash_driver,
                                              (By.ID, chart_card_id))
        assert chart_card.is_displayed()
        chart_card_body = wait_for_visible_element(dash_driver,
                                                   (By.ID, chart_card_body_id))
        assert chart_card_body.is_displayed()
        custom_placeholder = chart_card_body.find_element(
            By.CLASS_NAME, custom_placeholder_class)
        assert custom_placeholder.is_displayed()
        icon_placeholder = chart_card_body.find_element(
            By.CSS_SELECTOR, icon_placeholder_css)
        assert icon_placeholder.is_displayed()

    # Select a region from the dropdown
    ActionChains(dash_driver)\
        .click(region_dropdown)\
        .send_keys("England")\
        .send_keys(Keys.RETURN)\
        .pause(2)\
        .perform()

    # Verify the selected region value
    region_value_css = "#react-select-2--value-item"
    region_value = wait_for_visible_element(dash_driver,
                                            (By.CSS_SELECTOR, region_value_css)
                                            )
    assert region_value.text == "England"

    # Verify that the area chart is displayed
    area_chart = wait_for_visible_element(dash_driver,
                                          (By.ID, "stacked-area-chart"))
    assert area_chart.is_displayed()

    # Locate the year dropdown and verify its placeholder text
    year_dropdown = wait_for_clickable_element(dash_driver,
                                               (By.ID, "year-dropdown"))
    year_placeholder = year_dropdown.find_element(
        By.CSS_SELECTOR, ".Select-placeholder").text
    assert year_placeholder == "Select a year"

    # Select a year from the dropdown
    ActionChains(dash_driver)\
        .click(year_dropdown)\
        .send_keys("2021")\
        .send_keys(Keys.RETURN)\
        .pause(2)\
        .perform()

    # Verify the selected year value
    year_value_css = "#react-select-3--value-item"
    year_value = wait_for_visible_element(dash_driver,
                                          (By.CSS_SELECTOR, year_value_css))
    assert year_value.text == "2021"

    # Verify that the charts are displayed
    chart_ids = ['bar-chart', 'pie-chart', 'disparity-map']

    for chart_id in chart_ids:
        chart = wait_for_visible_element(dash_driver, (By.ID, chart_id))
        assert chart.is_displayed()

    # Clear the year selection and verify the placeholder text
    clear_year_selection_selector = (
        "#year-dropdown > div > div > span.Select-clear-zone > span"
    )
    clear_year_selection = wait_for_clickable_element(
        dash_driver, (By.CSS_SELECTOR, clear_year_selection_selector))
    clear_year_selection.click()
    placeholder_selector = "#year-dropdown .Select-placeholder"
    placeholder_element = wait_for_visible_element(
        dash_driver, (By.CSS_SELECTOR, placeholder_selector))
    assert placeholder_element.text == "Select a year"
