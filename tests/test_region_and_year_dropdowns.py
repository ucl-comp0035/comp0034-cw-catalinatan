from dash.testing.application_runners import import_app
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dash.testing.composite import DashComposite
import pytest


def test_region_and_year_dropdown(start_dash_app, dash_duo, dash_driver, wait_for_visible_element, wait_for_clickable_element): 
    """
    GIVEN the app is running
    WHEN the user selects a region and year
    THEN the region and year dropdowns should update 
    AND charts should be displayed 
    """
    region_dropdown = wait_for_clickable_element(dash_driver, (By.ID, "region-dropdown"))
    region_placeholder = region_dropdown.find_element(By.CSS_SELECTOR, ".Select-placeholder").text
    assert region_placeholder == "Select a region"

  
        lock_class_name = "custom-icon bi bi-lock"
    #     lock_icon_wait = wait_for_visible_element(dash_driver, (By.CLASS_NAME, lock_class_name))
    #     lock_icon_find = dash_driver.find_element(By.CLASS_NAME, lock_class_name)
    # except TimeoutException:
    #     pytest.fail("Lock icon did not become visible within the expected time")

    dash_driver.implicitly_wait(5)

    ActionChains(dash_driver)\
        .click(region_dropdown)\
        .pause(5)\
        .send_keys("England")\
        .pause(5)\
        .send_keys(Keys.RETURN)\
        .pause(5)\
        .perform()
    
    region_value_css = "#react-select-2--value-item"
    region_value = wait_for_visible_element(dash_driver, (By.CSS_SELECTOR, region_value_css))
    assert region_value.text == "England" 

    year_dropdown = wait_for_clickable_element(dash_driver, (By.ID, "year-dropdown"))
    year_placeholder = year_dropdown.find_element(By.CSS_SELECTOR, ".Select-placeholder").text
    assert year_placeholder == "Select a year"

    ActionChains(dash_driver)\
        .click(year_dropdown)\
        .pause(5)\
        .send_keys("2021")\
        .pause(5)\
        .send_keys(Keys.RETURN)\
        .pause(5)\
        .perform()

    year_value_css = "#react-select-3--value-item"
    year_value = wait_for_visible_element(dash_driver, (By.CSS_SELECTOR, year_value_css))
    assert year_value.text == "2021"

    WebDriverWait(dash_driver, 5).until(EC.invisibility_of_element_located((By.CLASS_NAME, lock_class_name)))
    # pie_chart = wait_for_visible_element(dash_driver, (By.CLASS_NAME, "custom-placeholder"))
    # assert pie_chart.get_attribute("src") != app.get_asset_url("pie_chart_placeholder.png")



    # pie_chart_card = wait_for_visible_element(dash_driver, (By.ID, 'pie-chart-card-content'))
    # pie_chart_graph = pie_chart_card.find_element(By.CSS_SELECTOR, ".dash-graph")
    # assert pie_chart_graph.is_displayed()

    # dash_duo.wait_for_element('#pie-chart-card-content .dash-graph', timeout=10)
    # graph = dash_duo.find_element('#pie-chart-card-content .dash-graph')
    # assert 'layout' in dash_duo.get_driver().execute_script(
    #     "return JSON.stringify(arguments[0].figure)", graph
    # ), "Graph should have valid figure data"
    # try: 
    #     area_chart_card = wait_for_visible_element(dash_driver, (By.ID, 'stacked-area-chart-card-content'))
    #     assert area_chart_card.is_displayed()
    # except TimeoutException:
    #     pytest.fail("Area chart card did not display within expected time")

    # ActionChains(dash_driver)\
    #     .click(year_dropdown)\
    #     .pause(5)\
    #     .send_keys("2021")\
    #     .pause(5)\
    #     .send_keys(Keys.RETURN)\
    #     .pause(5)\
    #     .perform()
    
    # try: 
    #     bar_chart_card = wait_for_visible_element(dash_driver, (By.ID, 'bar-chart-card-content'))
    #     assert bar_chart_card.is_displayed()
    #     pie_chart_card = wait_for_visible_element(dash_driver, (By.ID, 'pie-chart-card-content'))
    #     assert pie_chart_card.is_displayed()
    #     disparity_map_card = wait_for_visible_element(dash_driver, (By.ID, 'disparity-map-card-content'))
    #     assert disparity_map_card.is_displayed()
    # except TimeoutException:
    #     pytest.fail("Chart cards did not display within expected time")


    # chart_card_ids = ['bar-chart-card-content', 'pie-chart-card-content', 'disparity-map-card-content', 'stacked-area-chart-card-content']
    # icon_placeholder_css_list = ["#_dash-app-content > div > div:nth-child(4) > div:nth-child(2) > div > div > div > div:nth-child(1) > div > i"] * 4
    # chart_placeholder_css_list = [
    #     "#_dash-app-content > div > div:nth-child(3) > div:nth-child(1) > div > div > div > div:nth-child(1) > div > img",
    #     "#_dash-app-content > div > div:nth-child(3) > div:nth-child(2) > div > div > div > div:nth-child(1) > div > img",
    #     "#_dash-app-content > div > div:nth-child(4) > div:nth-child(1) > div > div > div > div:nth-child(1) > div:nth-child(1) > div > img",
    #     "#_dash-app-content > div > div:nth-child(4) > div:nth-child(2) > div > div > div > div:nth-child(1) > div > img"
    # ]

    # for chart_id, icon_placeholder_css, chart_placeholder_css in zip(chart_card_ids, icon_placeholder_css_list, chart_placeholder_css_list):
    #     try:
    #         # chart_card = wait_for_visible_element(dash_driver, (By.ID, chart_id), timeout=20)
    #         # assert chart_card.is_displayed()
    #     except:
    #         pytest.fail(f"{chart_id} did not display within expected time")
    # region_value = region_dropdown.get_attribute("value")
    # dash_duo.wait_for_text_to_equal("#region-dropdown", "England")
    # assert region_value == "England"

    # region_input = region_dropdown.find_element(By.CSS_SELECTOR, ".Select-input").text
    # assert region_input == "England"
    # assert region_placeholder == "Select a region"
    # region_placeholder = region_dropdown.find_element(By.CSS_SELECTOR, ".Select-placeholder").text
    # assert region_placeholder == "Select a region"
    # # Inner input for search value in dropdown
    # region_input = dash_duo.find_element("#region-dropdown input")

    
    
    # region_value = region_dropdown.get_attribute("value")
    # assert region_value == "England"

    # ActionChains(dash_driver)\
    #     .click(region_dropdown)\
    #     .pause(5)\
    #     .send_keys("x")

    # dash_duo.wait_for_text_to_equal(".Select-noresults", "No results found")

    # options = dash_duo.find_elements("#region-dropdown .VirtualizedSelectOption")
    # assert len(options) == 4

    # bar_chart_placeholder_css = "#_dash-app-content > div > div:nth-child(3) > div:nth-child(1) > div > div > div > div:nth-child(1) > div > img"
    # bar_chart_placeholder = wait_for_visible_element(dash_driver, (By.CSS_SELECTOR, bar_chart_placeholder_css))
    # assert bar_chart_placeholder.is_displayed()

    # lock_icon_placeholder_css = "#_dash-app-content > div > div:nth-child(3) > div:nth-child(1) > div > div > div > div:nth-child(1) > div > i"
    # lock_icon_placeholder = wait_for_visible_element(dash_driver, (By.CSS_SELECTOR, lock_icon_placeholder_css))
    # assert lock_icon_placeholder.is_displayed()
    
    # year_dropdown = wait_for_clickable_element(dash_driver, (By.ID, "year-dropdown"))
    # year_placeholder = year_dropdown.get_attribute("placeholder")

    # assert year_placeholder == "Select a year"

    # ActionChains(dash_driver)\
    #     .click(year_dropdown)\
    #     .pause(5)\
    #     .click("2021")\
    #     .pause(5)\
    #     .perform()
    
    # year_value = year_dropdown.get_attribute("value")
    # assert year_value == "2021" 

    # clear_year_selection_selector = "#year-dropdown > div > div > span.Select-clear-zone > span"
    # clear_year_selection = wait_for_clickable_element(dash_driver, (By.CSS_SELECTOR, clear_year_selection_selector))
    # clear_year_selection.click()
    # assert year_value == ""

