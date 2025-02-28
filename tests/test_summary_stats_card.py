from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def test_summary_stats_card(start_dash_app, dash_driver,
                            wait_for_clickable_element,
                            wait_for_visible_element):
    """
    GIVEN the app is running
    WHEN the user selects a region and year
    THEN the region and year dropdowns should update
    AND summary stats button should be displayed
    AND user can click summary stats button to view summary stats card
    AND user can click on the occupation stats tab to view occupation stats
    IF user changes region and year
    THEN summary stats will be updated
    AND occupation stats will reflect the new region and year
    """
    # Wait for the region dropdown to be clickable and select "England"
    region_dropdown = wait_for_clickable_element(
        dash_driver, (By.ID, "region-dropdown"))
    # Wait for the year dropdown to be clickable and select "2021"
    year_dropdown = wait_for_clickable_element(
        dash_driver, (By.ID, "year-dropdown"))

    # Perform actions to select "England" in the region dropdown and "2021" in
    # the year dropdown
    ActionChains(dash_driver)\
        .click(region_dropdown)\
        .send_keys("England")\
        .send_keys(Keys.RETURN)\
        .pause(2)\
        .click(year_dropdown)\
        .send_keys("2021")\
        .send_keys(Keys.RETURN)\
        .pause(2)\
        .perform()

    # Wait for the summary stats row to be visible and assert it is displayed
    summary_stats_row = wait_for_visible_element(
        dash_driver, (By.ID, "summary-stats-row"))
    assert summary_stats_row.is_displayed()

    # Wait for the summary stats column to be visible and assert it
    # is displayed
    summary_stats_column = wait_for_visible_element(
        dash_driver, (By.ID, "summary-stats-column"))
    assert summary_stats_column.is_displayed()

    # Define the CSS selector for the summary stats button and wait for it
    # to be visible
    display_summary_button_css = '#display-summary-button'
    summary_stats_button = wait_for_visible_element(
        dash_driver, (By.CSS_SELECTOR, display_summary_button_css))
    assert summary_stats_button.is_displayed()

    # Wait for the summary stats button to be clickable
    summary_stats_button = wait_for_clickable_element(
        dash_driver, (By.CSS_SELECTOR, display_summary_button_css))

    # Perform action to click the summary stats button
    ActionChains(dash_driver)\
        .click(summary_stats_button)\
        .pause(4)\
        .perform()

    # Wait for the occupation stats tab to be visible and assert
    # it is displayed
    occupation_stats_tab = wait_for_visible_element(
        dash_driver, (By.ID, "occupation-stats-tab"))
    assert occupation_stats_tab.is_displayed()

    # Perform action to click the occupation stats tab
    ActionChains(dash_driver)\
        .click(occupation_stats_tab)\
        .pause(2)\
        .perform()

    # Wait for the occupation location header to be visible and
    # assert it is displayed
    occ_location_header = wait_for_visible_element(
        dash_driver, (By.ID, "occ-location-header"))
    assert occ_location_header.is_displayed()

    # Get the text of the occupation location header and assert it
    # contains "England" and "2021"
    occ_location_header_text = occ_location_header.text
    assert "England" in occ_location_header_text
    assert "2021" in occ_location_header_text

    # Perform actions to change the region to "Scotland"
    ActionChains(dash_driver)\
        .click(region_dropdown)\
        .send_keys("Scotland")\
        .send_keys(Keys.RETURN)\
        .pause(2)\
        .perform()

    # Wait for the occupation location header to be visible and
    # assert it is displayed
    occ_location_header = wait_for_visible_element(
        dash_driver, (By.ID, "occ-location-header"))
    assert occ_location_header.is_displayed()

    # Get the text of the occupation location header and assert it
    # contains "Scotland"
    occ_location_header_text = occ_location_header.text
    assert "Scotland" in occ_location_header_text
