import geopandas as gpd
import pandas as pd

# the number of fires in each state is needed, within a year, and then, the map with this data is needed
gdf = gpd.read_file("WFIGS_Current_Interagency_Fire_Perimeters.geojson")
gdf.to_file("WFIGS_Interagency_Fire_Perimeters.geojson", driver="GeoJSON")

gdf_states = gpd.read_file("gz_2010_us_040_00_5m.json")
states_us = gdf["attr_POOState"]

gdf['state'] = states_us.replace(to_replace="US-", value="", regex=True)
gdf['month'] = gdf['attr_FireDiscoveryDateTime'].dt.month

gdf['acres'] = gdf['attr_IncidentSize']

tab = []
for i in states_us:
    if i not in tab:
        tab.append(i)

# print(tab)

sort = gdf.sort_values(by=['poly_IncidentName'])
sort2 = gdf['poly_IncidentName']
# print(sort)

tab_sort = []
for i in sort2:
    if i not in tab_sort:
        tab_sort.append(i)

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

df = pd.DataFrame(list(states.items()), columns=['STATE ID', 'FIRE'])
df.to_csv('df.csv', index=False)
# print(df.head())


numbers = {}
for state in states_us:
    if state in numbers:
        numbers[state] += 1
    else:
        numbers[state] = 1

# months = {}
# for i in states_us:
#     if gdf['months'] == 6:
#         months[i] += 1
#     else:
#         months[i] = 1
#
# print(months)

#sum of burnt areas per state
#jedynie potrzebna jest ta liczba elementów do zsumowania



#jesli wartosc jest = 0, to wtedy wywal to ze słownika
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

# number_to_months = {6: 'June',
#                     7: 'July',
#                     8: 'August',
#                     9: 'September',
#                     10: 'October'}
#
# gdf['month'] = gdf['month'].replace(number_to_months)
gdf_fires = gdf.groupby(['state', 'month']).acres.sum().reset_index()
gdf_fires['number of fires'] = gdf.groupby(['state', 'month']).acres.count().reset_index()['acres']
gdf_fires = gdf_fires.sort_values(by="month")
gdf_fires = gdf_fires.reset_index(drop=True)
gdf_fires.to_csv(f'gdf_fires.csv', index=False)
# print(gdf_fires.head())
    #
    # print(f"This is {i} month")
    # print(months.values(), '\n')
    #print(area, '\n')

    # months_df = pd.DataFrame(months_sum, index=[0])

    # print(months_df.head())
