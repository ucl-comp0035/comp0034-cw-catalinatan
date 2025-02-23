from dash import Output, Input, State, callback_context
from dash.dependencies import ALL, MATCH  # Add MATCH import
from dash.exceptions import PreventUpdate
from components import full_descriptions, df
import dash_bootstrap_components as dbc
from charts import (
    create_bar_chart,
    create_pie_chart,
    create_disparity_map,
    create_area_chart
)
from filter_data_functions import filter_dataframe, prepare_disparity_df, find_highest_dis_by_gender, find_overall_highest_disparity # Ensure prepare_year_disparity_df is imported
import json

def register_callbacks(app):
    """
    Register all callbacks for the Dash app.
    """
    @app.callback(
        Output("saved-analyses-menu", "children"),
        Output("saved-analyses-store", "data"),
        Input("save-filters-button", "n_clicks"),
        State("region-dropdown", "value"),
        State("year-dropdown", "value"),
        State("occupation-type-slider", "value"),
        State("saved-analyses-store", "data"),
        State("saved-analyses-menu", "children"),
        prevent_initial_call=True,
    )
    def save_filters(n_clicks, region, year, occupation, current_data, current_menu_items):
        if not n_clicks:
            raise PreventUpdate

        new_analysis = {
            "region": region,
            "year": year,
            "occupation": occupation
        }

        updated_data = current_data + [new_analysis]
        new_menu_item = dbc.DropdownMenuItem(
            f"Analysis {len(updated_data)}: {region}, {year}",
            id={"type": "saved-analysis", "index": len(updated_data)},
            n_clicks=0
        )

        return current_menu_items + [new_menu_item], updated_data

    @app.callback(
        [
            Output("region-dropdown", "value"),
            Output("year-dropdown", "value"),
            Output("occupation-type-slider", "value")
        ],
        [
            Input({"type": "saved-analysis", "index": ALL}, "n_clicks"),
            Input('clear-button', 'n_clicks')
        ],
        [
            State("saved-analyses-store", "data"),
            State('region-dropdown', 'value'),
            State('year-dropdown', 'value'),
            State('occupation-type-slider', 'value')
        ],
        prevent_initial_call=True,
    )

    def manage_dropdowns(saved_n_clicks, clear_n_clicks, data, region_value, year_value, occupation_value):
        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate

        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'clear-button':
            return None, None, 1

        try:
            triggered_id = json.loads(triggered_id)
            if triggered_id.get("type") == "saved-analysis":
                analysis_index = triggered_id["index"] - 1
                if 0 <= analysis_index < len(data):
                    analysis_data = data[analysis_index]
                    return analysis_data["region"], analysis_data["year"], analysis_data["occupation"]
        except json.JSONDecodeError:
            pass

        return region_value, year_value, occupation_value

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
    @app.callback(
        Output("selected-region", "children"),
        Output("selected-year", "children"),
        Input("region-dropdown", "value"),
        Input("year-dropdown", "value"),
    )
    def update_selected_filters(selected_region, selected_year):
        """
        Update the selected region, year and occupation based on the selected
        values.
        """

        if not selected_region or not selected_year:
            raise PreventUpdate

        return selected_region, selected_year
    
   
    @app.callback(
        Output("highest-disparity-region", "children"),
        Output("highest-disparity-percentage", "children"),
        Input("occupation-type-slider", "value"),
        Input("year-dropdown", "value"),
    )
    def update_highest_disparity_region(selected_occupation, selected_year):
        """
        Update the highest disparity region based on the selected occupation
        and year.
        """
        if not selected_occupation or not selected_year:
            raise PreventUpdate

        occupation_prefix = f"{selected_occupation}:"
        filtered_df = filter_dataframe(
            year=selected_year, occupation_prefix=occupation_prefix
        )
        disparity_df = prepare_disparity_df(filtered_df)

        highest_disparity_percentage = disparity_df['Disparity'].max()
        highest_disparity_perc_idx = disparity_df['Disparity'].idxmax()
        highest_disparity_region = disparity_df['Region'][highest_disparity_perc_idx]

        return highest_disparity_region, f"{highest_disparity_percentage:.2f}%"
    
    @app.callback(
        Output("highest-disparity-occupation", "children"),
        Output("highest-disparity-occupation-percentage", "children"),
        Input("region-dropdown", "value"),
        Input("year-dropdown", "value"),
        allow_duplicate=True
    )
    def update_highest_disparity_occupation_for_selected_region(selected_region, selected_year):
        """
        Update the highest disparity occupation based on the selected region
        and year.
        """
        if not selected_region or not selected_year:
            raise PreventUpdate

        filtered_df = filter_dataframe(region=selected_region, year=selected_year)
        disparity_df = prepare_disparity_df(filtered_df)

        highest_disparity_percentage = disparity_df['Disparity'].max()
        highest_disparity_perc_idx = disparity_df['Disparity'].idxmax()
        highest_disparity_occupation = disparity_df['Occupation Type'][highest_disparity_perc_idx]

        return highest_disparity_occupation, f"{highest_disparity_percentage:.2f}%"
    
    @app.callback(
        Output("highest-male-employment-occupation","children"),
        Output("highest-male-employment-percentage","children"),
        Input("region-dropdown","value"),
        Input("year-dropdown","value")
    )
    def update_highest_male_employment_occupation(selected_region, selected_year):
        """
        Update the highest male employment occupation based on the selected region
        and year.
        """
        if not selected_region or not selected_year:
            raise PreventUpdate
        
        male_df = filter_dataframe(region=selected_region, year=selected_year, gender='Male')

        highest_male_employment_percentage = male_df['Percentage Employed (Relative to Total Employment in the Year)'].max()
        highest_male_employ_perc_idx = male_df['Percentage Employed (Relative to Total Employment in the Year)'].idxmax()
        highest_male_employment_occupation = male_df['Occupation Type'][highest_male_employ_perc_idx]

        return highest_male_employment_occupation, f"{highest_male_employment_percentage:.2f}%"

    @app.callback(
        Output("highest-female-employment-occupation","children"),
        Output("highest-female-employment-percentage","children"),
        Input("region-dropdown","value"),
        Input("year-dropdown","value")
    )
    def update_highest_female_employment_occupation(selected_region, selected_year):
        """
        Update the highest female employment occupation based on the selected region
        and year.
        """
        if not selected_region or not selected_year:
            raise PreventUpdate
        
        female_df = filter_dataframe(region=selected_region, year=selected_year, gender='Female')

        highest_female_employment_percentage = female_df['Percentage Employed (Relative to Total Employment in the Year)'].max()
        highest_female_employ_perc_idx = female_df['Percentage Employed (Relative to Total Employment in the Year)'].idxmax()
        highest_female_employment_occupation = female_df['Occupation Type'][highest_female_employ_perc_idx]

        return highest_female_employment_occupation, f"{highest_female_employment_percentage:.2f}%"
    
    # Occupation disparity 
    @app.callback(
        Output("highest-m-year-disparity-percentage","children"),
        Output("highest-m-year-disparity-occupation","children"),
        Output("highest-m-year-disparity-region","children"),
        Output("highest-f-year-disparity-percentage","children"),
        Output("highest-f-year-disparity-occupation","children"),
        Output("highest-f-year-disparity-region","children"),
        Output("highest-year-disparity-gender","children"),
        Output("highest-year-disparity-region","children"),
        Input("region-dropdown","value")
    )
    def update_highest_total_employment_occupation(selected_region, selected_year):
        """
        Update the highest female employment occupation based on the selected region
        and year.
        """
        if not selected_region or not selected_year:
            raise PreventUpdate
        
        filtered_df = filter_dataframe(region=selected_region, year=selected_year)
        prepared_df = prepare_disparity_df(filtered_df)
        prepare_year_disparity_df = prepare_year_disparity_df(filtered_df)

        highest_total_employment_percentage = prepared_df['Total Employment'].max()
        highest_total_employ_perc_idx = prepared_df['Total Employment'].idxmax()
        highest_total_employment_occupation = prepared_df['Occupation Type'][highest_total_employ_perc_idx]

        highest_year_disparity_percentage = prepare_year_disparity_df['Year Disparity'].max()
        highest_year_disparity_perc_idx = prepare_year_disparity_df['Year Disparity'].idxmax()
        highest_year_disparity_occupation = prepare_year_disparity_df['Occupation Type'][highest_year_disparity_perc_idx]
        highest_year_disparity_gender = prepare_year_disparity_df['Gender'][highest_year_disparity_perc_idx]
        highest_year_disparity_region = prepare_year_disparity_df['Region'][highest_year_disparity_perc_idx]

        return highest_total_employment_occupation, f"{highest_total_employment_percentage:.2f}%", f"{highest_year_disparity_percentage:.2f}", highest_year_disparity_occupation, highest_year_disparity_gender, highest_year_disparity_region
    
    @app.callback(
        Output("summary-stats", "style"),
        Input("display-summary-button", "n_clicks"),
        prevent_initial_call=True
    )
    def toggle_summary_stats(n_clicks):
        """
        Toggle the display of summary statistics based on the button click.
        """
        if n_clicks % 2 == 1:
            return {"display": "block"}
        return {"display": "none"}

    @app.callback(
        Output("data_attribution","is_open"),
        Input("data-attribution-button","n_clicks")
    )

    def toggle_data_attribution(n_clicks, is_open):
        """
        Toggle the display of data attribution based on the button click.
        """
        if n_clicks:
            return not is_open
        return is_open
    