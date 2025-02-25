import pandas as pd
from pathlib import Path  # Correct import

# Create dataframe
data_path = Path(__file__).parent.parent / 'data' / 'employment_prepared.xlsx'
df = pd.read_excel(data_path)

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

def prepare_year_pivot_df(disparity_df):
    year_pivot_df = disparity_df.pivot_table(
        index=['Region', 'Occupation Type', 'Latitude', 'Longitude'],
        columns='Year',
        values='Total Employment',
        fill_value=0
    ).reset_index()

    year_pivot_df['Year Disparity'] = (year_pivot_df[2023] - year_pivot_df[2021])
    return year_pivot_df

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

def find_highest_dis_by_gender(df, gender, region=None):
    if region:
        df = df[df['Region'] == region]
    prepared_df = prepare_disparity_df(df)
    pivot_df = prepare_year_pivot_df(prepared_df)
    merged_df = prepared_df.merge(pivot_df[['Region','Occupation Type', 'Latitude', 'Longitude', 'Year Disparity']], on=['Region', 'Occupation Type', 'Latitude', 'Longitude'], how='left')
    melted_df = merged_df.melt(
        id_vars=['Region', 'Year', 'Occupation Type', 'Latitude', 'Longitude', 'Total Employment', 'Disparity', 'Year Disparity'],
        value_vars=['Male', 'Female'],
        var_name='Gender',
        value_name='Percentage Employed (Relative to Total Employment in the Year)'
    )
    specific_gender_df = melted_df[melted_df["Gender"] == gender]
    highest_absolute_year_disparity_perc = specific_gender_df['Year Disparity'].abs().max()
    highest_year_disparity_perc_idx = specific_gender_df['Year Disparity'].abs().idxmax()
    if specific_gender_df['Year Disparity'][highest_year_disparity_perc_idx] < 0:
        highest_year_disparity_percentage = f"-{highest_absolute_year_disparity_perc:.2f}"
    else:
        highest_year_disparity_percentage = f"{highest_absolute_year_disparity_perc:.2f}"
    highest_year_disparity_occupation = specific_gender_df['Occupation Type'][highest_year_disparity_perc_idx]
    highest_disparity_region = specific_gender_df['Region'][highest_year_disparity_perc_idx]
    return highest_year_disparity_percentage, highest_year_disparity_occupation, highest_disparity_region

def find_overall_highest_disparity(df, region=None):
    """
    Find the overall highest disparity between genders.

    Args:
        df (pd.DataFrame): The dataframe to search.

    Returns:
        tuple: The highest overall disparity percentage, occupation, region, and gender.
    """
    highest_male_disparity = find_highest_dis_by_gender(df, "Male", region)
    highest_female_disparity = find_highest_dis_by_gender(df, "Female", region)

    highest_male_disparity_perc = highest_male_disparity[0]
    highest_female_disparity_perc = highest_female_disparity[0]

    if float(highest_male_disparity_perc) > float(highest_female_disparity_perc):
        return highest_male_disparity + ("Male",)
    elif float(highest_male_disparity_perc) == float(highest_female_disparity_perc):
        return highest_male_disparity + ("Equal",)
    else:
        return highest_female_disparity + ("Female",)

highest_m_year_disparity_percentage, highest_m_year_disparity_occupation, highest_m_year_disparity_region = find_highest_dis_by_gender(df, "Male")
highest_f_year_disparity_percentage, highest_f_year_disparity_occupation, highest_f_year_disparity_region = find_highest_dis_by_gender(df, "Female")
highest_overall_disparity_percentage, highest_overall_disparity_occupation, highest_overall_disparity_region, highest_overall_disparity_gender = find_overall_highest_disparity(df)
