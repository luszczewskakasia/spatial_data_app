import os

import pytest

from get_data import *
import pandas as pd
gdf = gpd.read_file("WFIGS_Current_Interagency_Fire_Perimeters.geojson")

@pytest.fixture
def sample_df():
    sample_data = {
        "attr_POOState": ["PL-KR", 7, " ", "USA-AL"],
        "attr_FireDiscoveryDateTime": (['2023-12-01', 10, "xxx", '2023-02-02']),
        'attr_IncidentSize': ["10", "abc", 3, 0]
    }
    return pd.DataFrame(sample_data)

#passed
def test_set_states_name(sample_df):
    with pytest.raises(ValueError) as excinfo:
        set_state_names(sample_df)
    assert str(excinfo.value) == "State codes are incorrect"

#passed
def test_month(sample_df):
    with pytest.raises(ValueError) as excinfo:
        set_month(sample_df)
        print(sample_df)
    assert str(excinfo.value) == "Incorrect date format"

#passed
def test_set_acres(sample_df):
    with pytest.raises(ValueError) as excinfo:
        set_acres(sample_df)
    assert str(excinfo.value) == "Values are smaller than 0"


#there must be correct df. otherwise ValueError from setting state names rises
@pytest.fixture
def df_correct():
    sample_data = {
        "attr_POOState": ["US-KR", "US-AL"],
        "attr_FireDiscoveryDateTime": (['2023-12-01', '2023-02-02']),
        'attr_IncidentSize': [10, 25]
    }
    return pd.DataFrame(sample_data)

# passed
def test_make_dataframe(df_correct):
    result = make_dataframe(df_correct)
    assert isinstance(result, pd.DataFrame)


@pytest.fixture
def df_empty_values():
    sample_data = {
        "attr_POOState": ["US-CA", None,"US-AL"],
        "attr_FireDiscoveryDateTime": (['2023-12-01', '2023-02-02', None]),
        'attr_IncidentSize': [10, 25, None]
    }
    return pd.DataFrame(sample_data)

# doesn't work
def test_is_df_empty(df_empty_values):
    with pytest.raises(ValueError) as excinfo:
        make_dataframe(df_empty_values)
        print(make_dataframe(df_empty_values))
    assert str(excinfo.value) == "DataFrame has empty cells"


@pytest.fixture
def df_negative_values():
    sample_data = {
        "attr_POOState": ["US-CA", "US-AL"],
        "attr_FireDiscoveryDateTime": (['2023-12-01', '2023-02-02']),
        'attr_IncidentSize': ([10, -4])
    }
    return pd.DataFrame(sample_data)

#passed
def test_add_columns(df_negative_values):
    with pytest.raises(ValueError) as excinfo:
        add_columns(df_negative_values)
    assert str(excinfo.value) == "Values are smaller than 0"

#passed
def test_month_number_to_names():
    column_names = ['state','month','acres','number of fires','burnt area [km2]','state area [km2]','burnt area [%]','month_name']
    result = month_number_to_names(gdf)
    result_column_names = result.columns.to_list()
    assert column_names == result_column_names

#passed
def test_change_columns_order():
    column_names = ['state','month','acres','number of fires','burnt area [km2]','state area [km2]','burnt area [%]','month_name']
    result = month_number_to_names(gdf)
    result_column_names = result.columns.to_list()
    assert column_names == result_column_names
