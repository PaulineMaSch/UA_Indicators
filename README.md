# Urban Atlas Indicators

## Summary
The two python scripts will calculate the percentage of any Urban Atlas (UA) data within NUTS level-3 units. 'UA_Distribution.py' can be used for the 1-level categories of the UA. 'UA_Percentage.py' can be used for the UA codes, which is the lowest level of the UA data classification. 

## Set Up
1.	Clone the linked repository either via GitHub Desktop, Git Bash or download the ZIP file from GitHub.
2.	Launch Anaconda command prompt. If you still need to install Anaconda you can do so under this [link](https://www.anaconda.com/products/individual#Downloads).
3.	Navigate to the folder with the cloned repository and create a conda environment, running the following command `conda env create -f environment.yml`.
4.	Activate this environment with `conda activate UA_Indicators`.

## Main Dependencies
- python=3.8.8
- geopandas=0.9.0

## Data & Integration of other UA data set
The NUTS data from Eurostat is used in both scripts and can be found under the following [link](https://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts#nuts21).

The directory 'data_files' contains one test dataset from the UA data. To use another UA data set, download data under this [link](https://land.copernicus.eu/local/urban-atlas). The use of the UA data is free of charge, however a login is required. Extract the geopackage file from the download and save it to the directory 'data_files'. Remember to update the code (input data and variables) if you want to integrate other UA data. 

