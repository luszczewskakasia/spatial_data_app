import geopandas as gpd

# the number of fires in each state is needed, within a year, and then, the map with this data is needed
gdf = gpd.read_file("WFIGS_Current_Interagency_Fire_Perimeters.geojson")
states_us = gdf["attr_POOState"]

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

# print(len(areas))

numbers = {}
for state in states_us:
    if state in numbers:
        numbers[state] += 1
    else:
        numbers[state] = 1


# for state, count in numbers.items():
#     print(f' {state}: {numbers[state]}')
#
# months_sum = []
# for i in [6, 7, 8, 9, 10]:
#     months = {}
#     sorted_months = {}
#     for j in gdf['state']:
#         state_df = gdf[gdf['state'] == j]
#         appearance_sum = (state_df['month'] == i).sum()
#         months[j] = appearance_sum
#         months = {key: val for key, val in months.items() if val != 0}
#         months_keys = list(months.keys())
#         months_keys = sorted(months_keys)
#         sorted_months = {i: months[i] for i in months_keys}
#
#     for j in sorted_months.values():
#         months_sum.append(j)


def make_dataframe(gdf):
    states_us = gdf["attr_POOState"]
    gdf['state'] = states_us.replace(to_replace="US-", value="", regex=True)

    # retrieve month from timestamp
    gdf['month'] = gdf['attr_FireDiscoveryDateTime'].dt.month
    gdf['acres'] = gdf['attr_IncidentSize']

    # sum the area of fires per state in a certain month
    gdf_fires = gdf.groupby(['state', 'month']).acres.sum().reset_index()

    return gdf_fires


def add_columns(gdf_fires):
    # count the number of fires per month
    gdf_fires['number of fires'] = gdf.groupby(['state', 'month']).acres.count().reset_index()['acres']

    #  convert area to km2 from acres
    gdf_fires['burnt area [km2]'] = gdf_fires['acres'] * 0.004

    # assign size of the state to each column even if states are repeated in the dataframe
    gdf_fires['state area [km2]'] = gdf_fires['state'].map(areas, na_action='ignore')

    # show the scale of it in percents
    gdf_fires['burnt area [%]'] = (gdf_fires['burnt area [km2]'] / gdf_fires['state area [km2]']) * 100
    return gdf_fires


def month_number_to_names(gdf_fires):
    number_to_months = {6: 'June',
                        7: 'July',
                        8: 'August',
                        9: 'September',
                        10: 'October'}

    gdf_fires['month_name'] = gdf_fires['month'].map(number_to_months)

    return gdf_fires


def change_columns_order(gdf_fires):
    # improve readability of dataframe
    gdf_fires = gdf_fires.sort_values(by="month")
    gdf_fires = gdf_fires.reset_index(drop=True)
    return gdf_fires


def df_to_csv(gdf_fires):
    print(gdf_fires.columns.to_list())
    return gdf_fires.to_csv('df.csv',index=False)

gdf_fires = make_dataframe(gdf)
gdf_fires = add_columns(gdf_fires)
gdf_fires = month_number_to_names(gdf_fires)
gdf_fires = change_columns_order(gdf_fires)
df = df_to_csv(gdf_fires)