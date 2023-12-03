import pytest
from get_data import *
import pandas as pd


@pytest.fixture
# def df():
#     sample_data = {
#         'attr_POOState': ['US-AK', 'US-AK', 'US-CA', 'US-CA'],
#         'attr_FireDiscoveryDateTime': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-02-01', '2023-02-02']),
#         'attr_IncidentSize': [10, 15, 20, 25],
#     }
#     return pd.DataFrame(sample_data)

def df():
    test_gdf = pd.read_csv('df.csv')
    return pd.DataFrame(test_gdf)


def test_read_df(df):
    assert isinstance(df, pd.DataFrame)


def test_is_empty(df):
    if not df.empty:
        assert True


def test_df_columns(df):
    column_names = ['state', 'month', 'acres', 'number of fires', 'burnt area [km2]', 'state area [km2]',
                    'burnt area [%]', 'month_name']
    columns_df = df.columns.to_list()
    assert column_names == columns_df
