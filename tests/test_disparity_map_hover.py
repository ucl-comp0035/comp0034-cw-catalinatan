from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException)


def test_disparity_map_hover(start_dash_app,
                             dash_driver,
                             wait_for_visible_element,
                             wait_for_clickable_element):
    """
    GIVEN the app is running
    WHEN the user selects the year 2021 and moves the occupation type slider
    AND hovers over the disparity map
    THEN the tooltip should appear with the correct content
    """
    # Wait for the year dropdown to be clickable and select the year 2021
    year_dropdown = wait_for_clickable_element(
        dash_driver, (By.ID, "year-dropdown")
    )

    ActionChains(dash_driver)\
        .click(year_dropdown)\
        .send_keys("2021")\
        .send_keys(Keys.RETURN)\
        .pause(2)\
        .perform()

    # Wait for the occupation type slider to be visible
    occupation_type_slider = wait_for_visible_element(
        dash_driver, (By.ID, "occupation-type-slider")
    )

    # Calculate the position to click (5 out of 9 steps)
    slider_width = occupation_type_slider.size['width']
    click_position = slider_width * (5 - 1) / (9 - 1)

    # Create and perform the action chain to move the slider
    ActionChains(dash_driver)\
        .move_to_element(occupation_type_slider)\
        .move_by_offset(click_position - slider_width / 2, 0)\
        .click()\
        .pause(4)\
        .perform()

    # --- 2. Hover Logic ---
    def attempt_hover_and_verify():
        """
        Attempt to hover over the disparity map and verify the tooltip.

        Returns
        -------
        bool
            True if hover and verification are successful, False otherwise.
        """
        try:
            # Wait for the disparity map SVG element to be present
            wait = WebDriverWait(dash_driver, 20)
            disparity_map_svg = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#disparity-map svg")))

            # Get the location and size of the disparity map
            map_location = disparity_map_svg.location
            map_size = disparity_map_svg.size

            # Calculate the coordinates to hover over (England region)
            england_x = map_size['width'] * 0.4
            england_y = map_size['height'] * 0.6

            # Debugging: Print the values of england_x, england_y, map_size
            # and map_location
            print(f"england_x = {england_x}, england_y = {england_y}")
            print(f"map_size = {map_size}, map_location = {map_location}")

            # Move actions to the element, and move by offset inside
            actions = ActionChains(dash_driver)
            actions.move_to_element_with_offset(disparity_map_svg,
                                                england_x,
                                                england_y)
            actions.pause(1)  # Short pause might help
            actions.perform()

            # Wait for hovertext to appear
            hover_data = wait.until(EC.visibility_of_element_located(
                (By.CLASS_NAME, "hovertext")))

            # Verify the hovertext content
            assert "England" in hover_data.text
            assert "Disparity" in hover_data.text
            print("Successfully hovered and verified.")
            return True
        except (StaleElementReferenceException, TimeoutException,
                NoSuchElementException, AssertionError) as e:
            print(f"Hover or Verification Failed: {e}")
            return False

    # --- 3. Retry Mechanism ---
    max_attempts = 3
    for attempt in range(max_attempts):
        print(f"Attempt {attempt + 1} to hover and verify...")
        if attempt_hover_and_verify():
            print("Hover and verification successful!")
            return  # Exit if successful
        else:
            print("Retrying after a short pause...")
