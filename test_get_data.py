import pytest
from get_data import make_dataframe
import pandas as pd

@pytest.fixture
def df():
    sample_data = {
        'attr_POOState': ['US-AK', 'US-AK', 'US-CA', 'US-CA'],
        'attr_FireDiscoveryDateTime': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-02-01', '2023-02-02']),
        'attr_IncidentSize': [10, 15, 20, 25],
    }
    return pd.DataFrame(sample_data)

def test_make_dataframe(df):
    if df.empty:
        assert False

