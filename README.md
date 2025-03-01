## Test Suite

This project includes a comprehensive test suite to ensure the functionality and reliability of the application. The tests are written using `pytest` and `selenium` for end-to-end testing.

### Running the Tests

To run the tests, use the following command:

```bash
pytest
```

### Test Files

- `test_summary_stats_card.py`: Tests the summary stats card functionality.
- `test_server_live.py`: Tests if the server is live and responds correctly.
- `test_save_filters_callback.py`: Tests the save filters callback function.
- `test_region_and_year_dropdowns.py`: Tests the region and year dropdowns functionality.
- `test_disparity_map_hover.py`: Tests the hover functionality on the disparity map.
- `test_dataset_button.py`: Tests the dataset button and offcanvas interactions.
- `test_clear_analysis_callback.py`: Tests the clear analysis name callback function.
- `conftest.py`: Contains common fixtures for the tests.

### Setting Up a Virtual Environment

1. **Create a virtual environment**:
    ```sh
    python3 -m venv venv
    ```

2. **Activate the virtual environment**:
    - On macOS and Linux:
        ```sh
        source venv/bin/activate
        ```
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```

### Installing Dependencies
Before running the tests, make sure to install the necessary dependencies, including dash[testing] or dash\[testing]

```bash
pip install dash[testing]
```

```bash
pip install dash\[testing]
```

## Installing the Project
To install the project, use the following command:

```bash
pip install -e .
```

## Installing Additional Dependencies
To install additional dependencies listed in the requirements.txt file, use the following command:

```bash
pip install -r requirements.txt
```

## Source Files

The source files for this project are organized as follows:

- `app.py`: The main entry point for the Dash application. It sets up the app, layout, and callbacks.
- `layout.py`: Defines the layout of the Dash application, including the navigation bar, filters, buttons, and charts.
- `components.py`: Contains the reusable components used in the layout, such as dropdowns, buttons, and tooltips.
- `charts.py`: Contains functions to create various charts (bar chart, pie chart, disparity map, and area chart) using Plotly.
- `filter_data_functions.py`: Contains functions to filter and prepare the data for analysis and visualization.
- `callbacks.py`: Contains the callback functions to handle user interactions and update the app's components dynamically.
- `__init__.py`: Marks the directory as a package.

### Running the Application

To run the application, use the following command:

```bash
python src/app.py
```
