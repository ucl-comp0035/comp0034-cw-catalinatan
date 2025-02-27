from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict
from src.callbacks import update_tooltip


def test_update_tooltip():
    """
    GIVEN a Dash app with a occupation type slider
    WHEN the update_tooltip callback is triggered
    THEN check that the tooltip is updated
    """
    def run_callback(trigger, value):
        context_value.set(AttributeDict(**{"triggered_inputs": [trigger]}))
        return update_tooltip(value) 
    ctx = copy_context()

    trigger = {"prop_id": "occupation-type-slider.value"}
    value_range = {i: str(i) for i in range(1, 10)}
    full_descriptions = {
        1: "Managers, directors and senior officials",
        2: "Professional occupations",
        3: "Associate prof & tech occupations",
        4: "Administrative and secretarial occupations",
        5: "Skilled trades occupations",
        6: "Caring, leisure and other service occupations",
        7: "Sales and customer service occupations",
        8: "Process, plant and machine operatives",
        9: "Elementary occupations"
    }

    for value in value_range: 
        output = ctx.run(run_callback, trigger, value)
        expected_output = {
            'placement': 'bottom',
            'always_visible': True,
            'template': f"{full_descriptions[value]}"
        }
        assert output == expected_output

