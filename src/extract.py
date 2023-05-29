import pandas as pd
import netCDF4 as nc
from .plots import domain

def sst_fields(input_dir:str,file_name:str) -> nc._netCDF4.Dataset:
    # Reading the netCDF file.
    data = nc.Dataset(f'{input_dir}/{file_name}')
    # Printing the metadata.
    print(data)
    # Taking the necessary information to then close the netCDF file.
    sst = data['sst'][:].copy()
    # Making a plot redible plot of the file content.
    domain(data)
    data.close()
    return sst

def monthly_34_sst_avg(input_dir:str,file_name:str) -> pd.DataFrame:
    # Importing the data and putting the raw data ready to use.
    data = pd.read_csv(f'{input_dir}/{file_name}', header=None, sep=',')
    data.columns=['Year','Month', 'Anomaly (ºC)']
    return data

