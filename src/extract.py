import pandas as pd
import netCDF4 as nc
from .plots import domain

def sst_fields(input_dir:str,file_name:str) -> nc._netCDF4.Dataset:
    """
    This script extract the SST fields from the netCDF file. Also
    calls the "domain" function that plots the region studied in this 
    project.

    Parameters
    ----------
    input_dir: str
        directory where the data is located.
    file_name: str
        name of the netCDF file.
    
    Return
    ------
    sst: netCDF
        netCDF file object.
    """
    # Reading the netCDF file.
    data = nc.Dataset(f'{input_dir}/{file_name}')
    # Taking the necessary information to then close the netCDF file.
    sst = data['sst'][:].copy()
    domain(data)
    data.close()
    return sst

def monthly_34_sst_avg(input_dir:str,file_name:str) -> pd.DataFrame:
    """
    Extracts the data of a csv file containing information of the 
    Niño 3.4 region.

    Parameters
    ----------
    input_dir: str
        directory where the data is located.
    
    file_name: str
        name of the csv file.

    Returns
    -------
    data: pd.DataFrame
        a pandas DataFrame 
    """
    data = pd.read_csv(f'{input_dir}/{file_name}', header=None, sep=',')
    data.columns=['Year','Month', 'Anomaly (ºC)']
    return data

