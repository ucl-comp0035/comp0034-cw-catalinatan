from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict
from src.callbacks import update_tooltip


def test_update_tooltip():
    """
    GIVEN a Dash app with an occupation type slider and a tooltip callback
    WHEN the slider value changes
    THEN the tooltip is updated with the correct description
    """
    def run_callback(trigger, value):
        # Set the context value with the triggered input
        context_value.set(AttributeDict(**{"triggered_inputs": [trigger]}))
        # Call the update_tooltip function with the given value
        return update_tooltip(value)

    # Create a copy of the current context
    ctx = copy_context()

    # Define the trigger for the slider value change
    trigger = {"prop_id": "occupation-type-slider.value"}
    # Create a range of values for the slider
    value_range = {i: str(i) for i in range(1, 10)}
    # Define the full descriptions for each slider value
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

    # Iterate over each value in the value range
    for value in value_range:
        # Run the callback with the current context, trigger, and value
        output = ctx.run(run_callback, trigger, value)
        # Define the expected output for the current value
        expected_output = {
            'placement': 'bottom',
            'always_visible': True,
            'template': f"{full_descriptions[value]}"
        }
        # Assert that the output matches the expected output
        assert output == expected_output
