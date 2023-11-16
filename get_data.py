import geopandas as gpd
import pandas as pd

# the number of fires in each state is needed, within a year, and then, the map with this data is needed
gdf = gpd.read_file("WFIGS_Current_Interagency_Fire_Perimeters.geojson")

states_us = gdf["attr_POOState"]

gdf['state'] = states_us.replace(to_replace="US-", value="", regex=True)
gdf['month'] = gdf['attr_FireDiscoveryDateTime'].dt.month

gdf['acres'] = gdf['attr_IncidentSize']

areas_1 = {
    'AK': 131171,
    'AL': 1477953,
    'AR': 135771,
    'AZ': 294207,
    'CA': 403466,
    'CO': 268431,
    'CT': 12542,
    'DC': 158,
    'DE': 5047,
    'FL': 138887,
    'GA': 148959,
    'HI': 16635,
    'IA': 144669,
    'ID': 214045,
    'IL': 143793,
    'IN': 92789,
    'KS': 211754,
    'KY': 102269,
    'LA': 111898,
    'MA': 20202,
    'MD': 25142,
    'ME': 79883,
    'MI': 146435,
    'MN': 206232,
    'MO': 178040,
    'MS': 121531,
    'MT': 376962,
    'NC': 125920,
    'ND': 178711,
    'NE': 198974,
    'NH': 23187,
    'NJ': 19047,
    'NM': 314161,
    'NV': 284332,
    'NY': 122057,
    'OH': 105829,
    'OK': 177660,
    'OR': 248608,
    'PA': 115883,
    'RI': 2678,
    'SC': 77857,
    'SD': 196350,
    'TN': 106798,
    'TX': 676587,
    'UT': 212818,
    'VA': 23817,
    'VT': 23817,
    'WA': 172119,
    'WI': 140268,
    'WV': 62259,
    'WY': 251470
}

states = {
    'AK': '2',
    'AL': '1',
    'AR': '0',
    'AS': '0',
    'AZ': '5',
    'CA': '30',
    'CO': '4',
    'CT': '0',
    'DC': '0',
    'DE': '0',
    'FL': '0',
    'GA': '0',
    'GU': '0',
    'HI': '1',
    'IA': '0',
    'ID': '6',
    'IL': '1',
    'IN': '0',
    'KS': '0',
    'KY': '0',
    'LA': '5',
    'MA': '2',
    'MD': '0',
    'ME': '0',
    'MI': '1',
    'MN': '1',
    'MO': '0',
    'MP': '0',
    'MS': '1',
    'MT': '5',
    'NC': '0',
    'ND': '0',
    'NE': '0',
    'NH': '0',
    'NJ': '0',
    'NM': '1',
    'NV': '0',
    'NY': '0',
    'OH': '0',
    'OK': '0',
    'OR': '16',
    'PA': '0',
    'RI': '0',
    'SC': '0',
    'SD': '0',
    'TN': '0',
    'TX': '1',
    'UT': '1',
    'VA': '0',
    'VI': '0',
    'VT': '0',
    'WA': '1',
    'WI': '0',
    'WV': '0',
    'WY': '0'
}

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

df = pd.DataFrame(list(states.items()), columns=['STATE ID', 'FIRE'])
df.to_csv('df.csv', index=False)


numbers = {}
for state in states_us:
    if state in numbers:
        numbers[state] += 1
    else:
        numbers[state] = 1

months_sum = []
for i in [6, 7, 8, 9, 10]:
    months = {}
    sorted_months = {}
    for j in gdf['state']:
        state_df = gdf[gdf['state'] == j]
        appearance_sum = (state_df['month'] == i).sum()
        months[j] = appearance_sum
        months = {key: val for key, val in months.items() if val != 0}
        months_keys = list(months.keys())
        months_keys = sorted(months_keys)
        sorted_months = {i: months[i] for i in months_keys}

    for j in sorted_months.values():
        months_sum.append(j)

gdf_fires = gdf.groupby(['state', 'month']).acres.sum().reset_index()
gdf_fires['burnt area [km2]'] = gdf_fires['acres'] * 0.004
gdf_fires['number of fires'] = gdf.groupby(['state', 'month']).acres.count().reset_index()['acres']
gdf_fires['state area [km2]'] = gdf_fires['state'].map(areas, na_action='ignore')
gdf_fires['burnt area [%]'] = (gdf_fires['burnt area [km2]'] / gdf_fires['state area [km2]']) * 100
gdf_fires = gdf_fires.sort_values(by="month")
gdf_fires = gdf_fires.reset_index(drop=True)
gdf_fires = gdf_fires.reset_index(drop=True)
gdf_fires.to_csv(f'gdf_fires.csv', index=False)
