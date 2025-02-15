from dash import Output, Input, State, callback_context
from dash.exceptions import PreventUpdate
from components import full_descriptions, df
from charts import (
    create_bar_chart,
    create_pie_chart,
    create_disparity_map,
    create_area_chart
)
from filter_data_functions import filter_dataframe, prepare_disparity_df


def register_callbacks(app):
    """
    Register all callbacks for the Dash app.
    """

    @app.callback(
        Output('occupation-type-slider', 'tooltip'),
        Input('occupation-type-slider', 'value')
    )
    def update_tooltip(value):
        """
        Update the tooltip for the occupation type slider.
        """
        return {
            "placement": "bottom",
            "always_visible": True,
            "template": f"{full_descriptions[value]}"
        }

    @app.callback(
        [Output('region-dropdown', 'value'),
         Output('year-dropdown', 'value'),
         Output('occupation-type-slider', 'value')],
        Input('clear-button', 'n_clicks'),
        [State('region-dropdown', 'value'),
         State('year-dropdown', 'value'),
         State('occupation-type-slider', 'value')]
    )
    def manage_dropdowns(n_clicks, region_value, year_value, occupation_value):
        """
        Clear the dropdown selections when the clear button is clicked.
        """
        ctx = callback_context

        if not ctx.triggered:
            raise PreventUpdate

        if ctx.triggered[0]['prop_id'].split('.')[0] == 'clear-button':
            return None, None, 1

        return region_value, year_value, occupation_value

    @app.callback(
        Output('stacked-bar-chart', 'figure'),
        Input('region-dropdown', 'value'),
        Input('year-dropdown', 'value'),
    )
    def update_bar_chart(selected_region, selected_year):
        """
        Update the stacked bar chart based on the selected region and year.
        """
        if not selected_region or not selected_year:
            raise PreventUpdate

        df['Short Occupation Type'] = df['Occupation Type'] \
            .str.split(':').str[0]
        filtered_df = filter_dataframe(
            region=selected_region, year=selected_year)
        return create_bar_chart(filtered_df, selected_region, selected_year)

    @app.callback(
        Output('pie-chart', 'figure'),
        Input('region-dropdown', 'value'),
        Input('year-dropdown', 'value'),
    )
    def update_pie_chart(selected_region, selected_year):
        """
        Update the pie chart based on the selected region and year.
        """
        if not selected_region or not selected_year:
            raise PreventUpdate

        filtered_df = filter_dataframe(
            region=selected_region, year=selected_year)
        disparity_df = prepare_disparity_df(filtered_df)
        return create_pie_chart(disparity_df, selected_region, selected_year)

    @app.callback(
        Output("disparity-map", "figure"),
        Input("year-dropdown", "value"),
        Input("occupation-type-slider", "value"),
    )
    def update_map(selected_year, selected_occupation):
        """
        Update the disparity map based on the selected year and occupation
        type.
        """
        if not selected_year or not selected_occupation:
            raise PreventUpdate

        occupation_prefix = f"{selected_occupation}:"
        filtered_df = filter_dataframe(
            year=selected_year, occupation_prefix=occupation_prefix
        )
        disparity_df = prepare_disparity_df(filtered_df)
        disparity_df['Disparity'] = (
            disparity_df['Male'] - disparity_df['Female']
        ).abs()
        return create_disparity_map(disparity_df, selected_year)

    @app.callback(
        Output("stacked-area-chart", 'figure'),
        Input("region-dropdown", 'value'),
    )
    def update_area_chart(selected_region):
        """
        Update the stacked area chart based on the selected region.
        """
        if not selected_region:
            raise PreventUpdate

        filtered_df = filter_dataframe(region=selected_region)
        disparity_df = prepare_disparity_df(filtered_df)
        return create_area_chart(disparity_df, selected_region)
