import pytest
from dash import no_update
from dash.exceptions import PreventUpdate
from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict
from src.callbacks import save_filters
import dash_bootstrap_components as dbc

# References:
# https://plotly.com/blog/building-unit-tests-for-dash-applications/


@pytest.mark.parametrize(
    "n_clicks, custom_analysis_name, region, year, occupation, current_data,"
    "current_menu_items, expected_output",
    [
        # Test case 1: Save a new analysis with a custom name
        (
            1, "Test Analysis", "Scotland", 2021, "1", [], [],
            (
                [
                    dbc.DropdownMenuItem(
                        children='Test Analysis',
                        id={'type': 'saved-analysis', 'index': 0},
                        n_clicks=0
                    )
                ],
                [
                    {
                        "name": "Test Analysis",
                        "region": "Scotland",
                        "year": 2021,
                        "occupation": "1"
                    }
                ],
                False,
                no_update
            )
        ),

        # Test case 2: Save a new analysis with the default name
        (1, "", "England", 2023, "3", [], [], (
            [
                dbc.DropdownMenuItem(
                    children='Analysis 1: England, 2023',
                    id={'type': 'saved-analysis', 'index': 0},
                    n_clicks=0
                )
            ],
            [
                {
                    "name": "Analysis 1: England, 2023",
                    "region": "England",
                    "year": 2023,
                    "occupation": "3"
                }
            ],
            False,
            no_update
        )),

        # Test case 3: Prevent saving an analysis without selecting a
        # region and year
        (1, "", "", 2021, "1", [], [], (
            no_update,
            no_update,
            True,
            "Please select a region and year before saving an analysis."
        )),

        # Test case 4: Prevent saving an analysis with a duplicate name
        (1, "Test Analysis", "Scotland", 2021, "1", [
            {
                "name": "Test Analysis",
                "region": "Scotland",
                "year": 2021,
                "occupation": "1"
            }
        ], [
            {
                "type": "saved-analysis",
                "index": 0,
                "children": "Test Analysis"
            }
        ], (
            no_update,
            no_update,
            True,
            (
                "An analysis named 'Test Analysis' already exists. "
                "Please choose a different name."
            )
        )),

        # Test case 5: Prevent saving an analysis without clicking the
        # save button
        (0, "", "", "", "", "", [], (
            PreventUpdate,
            PreventUpdate,
            PreventUpdate,
            PreventUpdate
        ))
    ]
)
def test_save_filters(
        n_clicks,
        custom_analysis_name,
        region,
        year,
        occupation,
        current_data,
        current_menu_items,
        expected_output):
    """
    Test the save_filters callback function with various scenarios.
    """

    def run_callback():
        """
        Run the save_filters callback function within a copied context.
        """
        context_value.set(
            AttributeDict(
                **{
                    "triggered_inputs": [
                        {"prop_id": "save-filters-button.n_clicks"}
                    ]
                }
            )
        )
        return save_filters(
            n_clicks, custom_analysis_name, region, year, occupation,
            current_data, current_menu_items
        )

    ctx = copy_context()

    if n_clicks == 0:
        # Test case where the save button is not clicked
        with pytest.raises(PreventUpdate):
            ctx.run(run_callback)
    else:
        output = ctx.run(run_callback)

        if isinstance(expected_output, tuple):
            output = ctx.run(run_callback)
            # Compare the properties of the DropdownMenuItem objects
            output_menu_items = output[0]
            expected_menu_items = expected_output[0]

            if expected_menu_items == no_update:
                assert output_menu_items == expected_menu_items
            else:
                for output_item, expected_item in zip(output_menu_items,
                                                      expected_menu_items):
                    assert output_item.children == expected_item.children
                    assert output_item.id == expected_item.id
                    assert output_item.n_clicks == expected_item.n_clicks

            assert output[1:] == expected_output[1:]
