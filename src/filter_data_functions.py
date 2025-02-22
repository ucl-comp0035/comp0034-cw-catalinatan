from components import df


def filter_dataframe(region=None, year=None, occupation_prefix=None, gender=None):
    """
    Filter the dataframe based on the provided region, year, and occupation prefix.

    Args:
        region (str, optional): The region to filter by.
        year (int, optional): The year to filter by.
        occupation_prefix (str, optional): The occupation prefix to filter by.

    Returns:
        pd.DataFrame: The filtered dataframe.
    """
    filtered_df = df.copy()
    if region:
        filtered_df = filtered_df[filtered_df['Region'] == region]
    if year:
        filtered_df = filtered_df[filtered_df['Year'] == int(year)]
    if occupation_prefix:
        filtered_df = filtered_df[filtered_df['Occupation Type'].str.startswith(occupation_prefix)]
    if gender:
        filtered_df = filtered_df[filtered_df['Gender'] == gender]
    return filtered_df


def prepare_disparity_df(filtered_df):
    """
    Prepare the disparity dataframe by pivoting and calculating total employment.

    Args:
        filtered_df (pd.DataFrame): The filtered dataframe.

    Returns:
        pd.DataFrame: The prepared disparity dataframe.
    """
    disparity_df = filtered_df.pivot_table(
        index=['Region', 'Year', 'Occupation Type', 'Latitude', 'Longitude'],
        columns='Gender',
        values='Percentage Employed (Relative to Total Employment in the Year)',
        fill_value=0
    ).reset_index()
    disparity_df['Total Employment'] = disparity_df['Male'] + disparity_df['Female']
    disparity_df['Disparity'] = (
            disparity_df['Male'] - disparity_df['Female']
        ).abs()
    return disparity_df