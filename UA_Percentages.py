import geopandas as gpd

# load data, choose one option for the UA data depending on the data type
UA = gpd.read_file('data_files/UK008L3_GREATER_MANCHESTER_UA2012_revised_v021.gpkg', layer='UK008L3_GREATER_MANCHESTER_UA2012_revised')
#UA = gpd.read_file('data_files/test_UA12_Ruhr.shp')
Nuts3 = gpd.read_file('data_files/NUTS_RG_01M_2021_3035_LEVL_3.shp')
Nuts3midpoint = gpd.read_file('data_files/NUTS_LB_2021_3035_LEVL_3.shp')

# variables to update based on dataset
Pop = 'Pop2012'
Code = 'code_2012'
Area = 'GTM'

# selecting the rows in the Nuts3 data set that make up the UA area
Nuts3_mid_UA = gpd.sjoin(Nuts3midpoint, UA, op="within", how="left")
Nuts3_mid_Area = Nuts3_mid_UA[Nuts3_mid_UA[Pop] >=0]
Nuts3_mid_Area = Nuts3_mid_Area.drop(['index_right'], axis=1)

Nuts3_Area = gpd.sjoin(Nuts3, Nuts3_mid_Area, how='left', op='contains')
Nuts3_Area = Nuts3_Area[Nuts3_Area[Pop] >=0]

# clearing the gdf by deleting unnecessary columns
Nuts3_Area.drop(Nuts3_Area.columns[10:], axis=1, inplace=True)

# calculating the area of the Nuts3 units in sqkm
Nuts3_Area['Area_Nuts'] = Nuts3_Area['geometry'].area /10**6

# intersect the UA data with the Nuts3 data and then calculating area in sqm of UA data
UA_Nuts3 = gpd.overlay(UA, Nuts3_Area, how='intersection')
UA_Nuts3['Area_UA'] = UA_Nuts3['geometry'].area

# function that can be passed arbitrary number of UA land use codes and will calculate their percentage on the
# Nuts3 unit either separately or jointly
def Code_Perc(*uacode, join=False):
    global Nuts3_Area
    if join == True:
        for ua in uacode:
            UA_Category = UA_Nuts3[UA_Nuts3[Code] == ua].groupby(['NUTS_ID_left', Code])['Area_UA'].sum().reset_index(name=ua + '_Area_Sum')
            UA_Category[ua + '_Area_Sum'] = UA_Category[ua + '_Area_Sum'] / 10 ** 6  # to get sqkm
            Nuts3_Area = Nuts3_Area.merge(UA_Category, on='NUTS_ID_left', how='left')
            del Nuts3_Area[Code]
        Nuts3_Area['Join_Area_Sum'] = Nuts3_Area.loc[:,Nuts3_Area.columns.str.endswith('_Area_Sum')].sum(axis=1)
        Nuts3_Area['Join_Percentage'] = Nuts3_Area['Join_Area_Sum'] / Nuts3_Area['Area_Nuts'] * 100
    else:
        for ua in uacode:
            UA_Category = UA_Nuts3[UA_Nuts3[Code] == ua].groupby(['NUTS_ID_left',Code])['Area_UA'].sum().reset_index(name=ua+'_Area_Sum')
            UA_Category[ua+'_Area_Sum'] = UA_Category[ua+'_Area_Sum'] / 10 ** 6  # to get sqkm
            Nuts3_Area = Nuts3_Area.merge(UA_Category, on='NUTS_ID_left', how='left')
            Nuts3_Area[ua+'_Percentage'] = Nuts3_Area[ua+'_Area_Sum'] / Nuts3_Area['Area_Nuts'] * 100

# run the function with the desired UA code(s)
Code_Perc('14100','50000',join=True)

# several output options, remove '#' based on your preferred outcome

# show results directly
# print(Nuts3_Area)
# print(Nuts3_Area.columns)

# export to file
Nuts3_Area.to_excel(excel_writer=Area+'_UA_Percentages.xlsx')
#Nuts3_Area.to_file(filename = Area+'_UA_Percentages.shp')

# visualize results geographically
# ...to be inserted








