import geopandas as gpd
import numpy as np
import pandas as pd

gdf = gpd.read_file("WFIGS_Current_Interagency_Fire_Perimeters.geojson")


def set_state_names(gdf):
    """
    Extracts state names from the 'attr_POOState' column of a GeoDataFrame.

    Parameters:
    gdf (geopandas.GeoDataFrame): Input GeoDataFrame containing fire perimeter data.

    Returns:
    pandas.Series: Series containing state names.

    Raises:
    ValueError: If state codes are incorrect.
    """

    states_us = gdf["attr_POOState"]
    if states_us.str.startswith("US-").any():
        gdf['state'] = states_us.replace(to_replace="US-", value="", regex=True)
    else:
        raise ValueError("State codes are incorrect")

    return gdf['state']


def set_month(gdf):

    """
    Extracts months from the 'attr_FireDiscoveryDateTime' column of a GeoDataFrame.

    Parameters:
    gdf (geopandas.GeoDataFrame): Input GeoDataFrame containing fire perimeter data.

    Returns:
    pandas.Series: Series containing month values.

    Raises:
    ValueError: If date format is incorrect.
    """
    try:
        gdf['month'] = pd.to_datetime(gdf['attr_FireDiscoveryDateTime'], format='%Y-%m-%d')
        gdf['month'] = gdf['month'].dt.month
        return gdf['month']
    except ValueError:
        raise ValueError("Incorrect date format")


def set_acres(gdf):
    """
    Converts 'attr_IncidentSize' column values to float.

    Parameters:
    gdf (geopandas.GeoDataFrame): Input GeoDataFrame containing fire perimeter data.

    Returns:
    pandas.Series: Series containing float values representing acres.

    Raises:
    ValueError: If values in 'attr_IncidentSize' are not numbers.
    """
    try:
        gdf['acres'] = gdf['attr_IncidentSize'].astype(float)
        return gdf['acres']
    except:
        raise ValueError("Values are not numbers")


def make_dataframe(gdf):
    """
    Creates a DataFrame with aggregated fire data by state and month.

    Parameters:
    gdf (geopandas.GeoDataFrame): Input GeoDataFrame containing fire perimeter data.

    Returns:
    pandas.DataFrame: DataFrame with aggregated fire data.

    Raises:
    ValueError: If the DataFrame has empty cells.
    """
    try:
        gdf['state'] = set_state_names(gdf)
        gdf['month'] = set_month(gdf)
        gdf['acres'] = set_acres(gdf)

        # sum the area of fires per state in a certain month
        gdf_fires = gdf.groupby(['state', 'month']).acres.sum().reset_index()
        # count the number of fires per month
        gdf_fires['number of fires'] = gdf.groupby(['state', 'month']).acres.count().reset_index()['acres']

        # return gdf_fires

        if all(item != "" and item is not None and item != np.NaNdo  for item in gdf_fires['acres']):
            return gdf_fires

    except Exception:
        raise ValueError("DataFrame has empty cells")


def add_columns(gdf):
    """
    Adds additional columns to the DataFrame, including burnt area in km2, state area, and burnt area in %.

    Parameters:
    gdf (geopandas.GeoDataFrame): Input GeoDataFrame containing fire perimeter data.

    Returns:
    pandas.DataFrame: DataFrame with additional columns.

    Raises:
    ValueError: If values in 'acres' are smaller than 0.
    """
    gdf_fires = make_dataframe(gdf)
    #  convert area to km2 from acres
    gdf_fires['burnt area [km2]'] = gdf_fires['acres'] * 0.004
    # dict with area of each state in the df
    areas = {
        'AK': 131171,
        'AL': 1477953,
        'AZ': 294207,
        'CA': 403466,
        'CO': 268431,
        'HI': 16635,
        'ID': 214045,
        'IL': 143793,
        'LA': 111898,
        'MA': 20202,
        'MI': 146435,
        'MN': 206232,
        'MS': 121531,
        'MT': 376962,
        'NM': 314161,
        'OR': 248608,
        'TX': 676587,
        'UT': 212818,
        'WA': 172119,
    }
    # assign size of the state to each column even if states are repeated in the dataframe
    gdf_fires['state area [km2]'] = gdf_fires['state'].map(areas, na_action='ignore')

    # show the scale of it in percents
    gdf_fires['burnt area [%]'] = (gdf_fires['burnt area [km2]'] / gdf_fires['state area [km2]']) * 100

    if any(item <= 0 for item in gdf_fires['acres']):
        raise ValueError("Values are smaller than 0")

    return gdf_fires

def month_number_to_names(gdf):
    """
    Converts month values written in numbers to month names.

    Parameters:
    gdf (geopandas.GeoDataFrame): Input GeoDataFrame containing fire perimeter data.

    Returns:
    pandas.DataFrame: DataFrame with 'month_name' column.

    Raises:
    Exception: If an error occurs during the conversion.
    """
    try:
        gdf_fires = add_columns(gdf)
        number_to_months = {6: 'June',
                            7: 'July',
                            8: 'August',
                            9: 'September',
                            10: 'October'}

        gdf_fires['month_name'] = gdf_fires['month'].map(number_to_months)

        return gdf_fires
    except:
        return None

def change_columns_order(gdf):
    """
    Sorts and resets the index of the DataFrame for improved readability.

    Parameters:
    gdf (geopandas.GeoDataFrame): Input GeoDataFrame containing fire perimeter data.

    Returns:
    pandas.DataFrame: DataFrame with sorted columns and reset index.

    Raises:
    Exception: If an error occurs during the sorting.
    """
    try:
        gdf_fires = add_columns(gdf)
        gdf_fires = gdf_fires.sort_values(by="month")
        gdf_fires = gdf_fires.reset_index(drop=True)
        return gdf_fires
    except:
        return None



def df_to_csv(gdf, file_path='df.csv'):
    """
    Converts the DataFrame to a CSV file.

    Parameters:
    gdf (geopandas.GeoDataFrame): Input GeoDataFrame containing fire perimeter data.
    file_path (str): Path to the output CSV file.

    Returns:
    str: File path of the generated CSV.

    Raises:
    TypeError: If the file path is invalid.
    """
    try:
        gdf_fires = change_columns_order(gdf)
        gdf_fires.to_csv(file_path, index=False)
        return file_path
    except Exception:
        raise TypeError("Invalid path")


if __name__ == '__main__':
    print(change_columns_order(gdf))