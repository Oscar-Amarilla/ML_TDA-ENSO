"""
Here is all the necessary information related to input/output files 
and directories so as not to directly metion them in the main codes.
"""
from pathlib import Path

INPUT_DIR = str(Path.cwd() / "input")
OUTPUT_DIR = str(Path.cwd() / "outputs")

class FILES:

    def __init__(self) ->None:
        self.nc_file = 'cobe2_sst_mon_mean.nc'
        self.csv_file = 'nino34.csv'

    
