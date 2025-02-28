from dash import no_update
from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict
from src.callbacks import clear_analysis_name


def test_clear_analysis_name_with_one_click():
    """
    GIVEN a Dash app with a specified analysis name in the session
    WHEN the clear_analysis_name callback is triggered
        1. with one click
        2. with zero clicks
    THEN check that the analysis name is cleared from the session for one click
         and no update occurs for zero clicks
    """
    def run_callback(trigger, n_clicks):
        # Set the context value with the triggered inputs
        context_value.set(AttributeDict(**{"triggered_inputs": [trigger]}))
        # Run the clear_analysis_name callback with the given number of clicks
        return clear_analysis_name(n_clicks)

    # Create a copy of the current context
    ctx = copy_context()

    # Define the trigger and number of clicks for the first test case
    trigger = {"prop_id": "save-filters-button.n_clicks"}
    n_clicks = 1

    # Run the callback in the copied context and check the output
    output = ctx.run(run_callback, trigger, n_clicks)
    assert output == ""

    # Define the trigger and number of clicks for the second test case
    trigger = []
    n_clicks = 0

    # Run the callback in the copied context and check the output
    output = ctx.run(run_callback, trigger, n_clicks)
    assert output == no_update
