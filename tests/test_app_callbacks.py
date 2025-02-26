from dash import no_update
from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict
from src.callbacks import update_tooltip, clear_analysis_name, toggle_data_attribution


def test_clear_analysis_name_with_one_click():
    """
    GIVEN a Dash app with a specified analysis name in the session
    WHEN the clear_analysis_name callback is triggered with one click
    THEN check that the analysis name is cleared from the session
    """
    def run_callback():
        context_value.set(AttributeDict(**{"triggered_inputs": [{"prop_id": "save-filters-button.n_clicks"}]
                                           }))
        return clear_analysis_name(1)
    
    ctx = copy_context()
    output = ctx.run(run_callback)
    assert output == ""

def test_clear_analysis_name_initial_state():
    """
    GIVEN a Dash app with a specified analysis name in the session
    WHEN the clear_analysis_name callback is triggered with no clicks
    THEN check that the analysis name remains unchanged
    """
    def run_callback():
        context_value.set(AttributeDict(**{"triggered_inputs": []
                                           }))
        return clear_analysis_name(None)

    ctx = copy_context()
    output = ctx.run(run_callback)
    assert output == no_update


def test_update_tooltip():
    """
    GIVEN a Dash app with a occupation type slider
    WHEN the update_tooltip callback is triggered
    THEN check that the tooltip is updated
    """
    def run_callback():
        context_value.set(AttributeDict(**{"triggered_inputs": [{"prop_id": "occupation-type-slider.value"}]}))
        return update_tooltip(3) # 3 is the value of the occupation type slider
    
    ctx = copy_context()
    output = ctx.run(run_callback)
    assert output == "Associate prof & tech occupations"


def test_toggle_data_attribution_with_one_click():
    """GIVEN a Dash app with a data attribution toggle
    WHEN the toggle_data_attribution callback is triggered
    THEN check that the data attribution is displayed"""
    def run_callback(is_open):
        context_value.set(AttributeDict(**{
            "triggered_inputs": [{"prop_id": "data-attribution-button.n_clicks"}],
            "states": {"data-attribution-canvas.is_open": is_open}
        }))
        return toggle_data_attribution(1, is_open)
    
    ctx = copy_context()
    output = ctx.run(run_callback)
    assert output == True

def test_toggle_data_attribution_initial_state():
    """GIVEN a Dash app with a data attribution toggle
    WHEN the toggle_data_attribution callback is triggered with no click
    THEN check that the data attribution is not displayed"""
    def run_callback(is_open):
        context_value.set(AttributeDict(**{
            "triggered-inputs": [],
            "statest": {"data-attribution-canvas.is_open": is_open}
        }))
        return toggle_data_attribution(None, is_open) 
    
    ctx = copy_context()
    output = ctx.run(run_callback)
    assert output == False



