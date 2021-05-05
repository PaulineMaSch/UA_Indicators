import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

# load data, choose one option for the UA data depending on the data type
#UA = gpd.read_file('data_files/filename.gpkg', layer='layername')
UA = gpd.read_file('data_files/test_UA12_Ruhr.shp')
Nuts3 = gpd.read_file('data_files/NUTS_RG_01M_2021_3035_LEVL_3.shp')
Nuts3midpoint = gpd.read_file('data_files/NUTS_LB_2021_3035_LEVL_3.shp')

# variables to update based on dataset
Pop = 'Pop2012'
Code = 'CODE2012'
Area = 'Ruhr'

# overall task: calculate percentage of overall UA land use category per Nuts3 unit

# selecting the rows in the Nuts3 data set that make up the UA area
Nuts3_mid_UA = gpd.sjoin(Nuts3midpoint, UA, op="within", how="left")
Nuts3_mid_Area = Nuts3_mid_UA[Nuts3_mid_UA[Pop] >=0]
Nuts3_mid_Area = Nuts3_mid_Area.drop(['index_right'], axis=1)

Nuts3_Area = gpd.sjoin(Nuts3, Nuts3_mid_Area, how='left', op='contains')
Nuts3_Area = Nuts3_Area[Nuts3_Area[Pop] >=0]

# cleaning the gdf by deleting unnecessary columns
Nuts3_Area.drop(Nuts3_Area.columns[10:], axis=1, inplace=True)

# calculating the area of the Nuts3 units in sqkm
Nuts3_Area['Area_Nuts'] = Nuts3_Area['geometry'].area /10**6

# intersect the UA data with the Nuts3 data and then calculating area in sqm of UA data
UA_Nuts3 = gpd.overlay(UA, Nuts3_Area, how='intersection')
UA_Nuts3['Area_UA'] = UA_Nuts3['geometry'].area

# reclassifying the landuse column with the UA Code in their overlaying 5 categories (cf. documentation) in a new column
UA_Nuts3['UA_Category'] = UA_Nuts3[Code].str[0]

# group by the new 'UA_Category' column and the 'NUTS_ID_left' while summing up the area of the UA features in each
# category for the individual cities and resetting the index
UA_Category = UA_Nuts3.groupby(['NUTS_ID_left','UA_Category'])['Area_UA'].sum().reset_index(name='UA_Area_Sum')
UA_Category['UA_Area_Sum'] = UA_Category['UA_Area_Sum'] /10**6 # to get sqkm

# select one category after each other and join it as a new column to the Nuts3_Area gdf
for category in UA_Category['UA_Category'].unique():
    Nuts3_Area = Nuts3_Area.merge(UA_Category[UA_Category['UA_Category'] == category], on='NUTS_ID_left', how='left')
    Nuts3_Area = Nuts3_Area.rename(columns={'UA_Area_Sum': 'UA_'+category+'_Area'})
    del Nuts3_Area['UA_Category']

# calculate the percentage of each UA category in the individual Nuts3 units
for column in Nuts3_Area.columns[11:]:
   Nuts3_Area['perc_'+column] = Nuts3_Area[column]/Nuts3_Area['Area_Nuts']*100

# several output options, remove '#' based on your preferred output

# show results directly
# print(Nuts3_Area)
# print(Nuts3_Area.columns)

#Nuts3_Area.to_excel(excel_writer=Area+'_UA_Distribution.xlsx') # export to excel
#Nuts3_Area.to_file(filename = Area+'_UA_Distribution.shp') # export to shapefile

# visualize results graphically
def plot_results():
    plot_array = Nuts3_Area.loc[:,Nuts3_Area.columns.str.startswith('perc_')].to_numpy()
    plot_array_T = plot_array.T # invert columns and rows
    label_array = Nuts3_Area['NUTS_NAME_left'] #to get NUTS3 units to label x-axis

    colors = ['lightcoral','khaki', 'seagreen','steelblue','mediumaquamarine']
    Pos = range(len(plot_array_T[0]))

    for i in range(len(plot_array_T)):
        plt.bar(Pos, plot_array_T[i], bottom=np.sum(plot_array_T[:i], axis=0), color= colors[i % len(colors)])

    plt.xticks(Pos, label_array,rotation = 20,ha='right')
    plt.legend(['1: Artificial Surfaces','2: Agricultural Areas','3: Natural Areas','5: Water','4: Wetlands']
               ,bbox_to_anchor=(0,1.02,1,0.2), loc="lower center", borderaxespad=0, ncol=2)
    plt.savefig(fname=Area + '_UA_Distribution.png', bbox_inches = 'tight')
    plt.show()

#plot_results() #show and export stacked bar chart


