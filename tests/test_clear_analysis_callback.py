from dash import no_update
from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict
from src.callbacks import clear_analysis_name


def test_clear_analysis_name_with_one_click():
    """
    GIVEN a Dash app with a specified analysis name in the session
    WHEN the clear_analysis_name callback is triggered with one click
    THEN check that the analysis name is cleared from the session
    """
    def run_callback(trigger, n_clicks):
        context_value.set(AttributeDict(**{"triggered_inputs": [trigger]
                                           }))
        return clear_analysis_name(n_clicks)
    ctx = copy_context()

    trigger = {"prop_id": "save-filters-button.n_clicks"}
    n_clicks = 1
    output = ctx.run(run_callback, trigger, n_clicks)
    assert output == ""

    trigger = []
    n_clicks = 0
    output = ctx.run(run_callback, trigger, n_clicks)
    assert output == no_update