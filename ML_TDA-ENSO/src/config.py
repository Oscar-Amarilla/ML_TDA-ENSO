from pathlib import Path

INPUT_DIR = str(Path.cwd() / "input")

class FILES:

    def __init__(self) ->None:
        self.nc_file = 'sst_mon_mean.nc'
        self.csv_file = 'month_34_data.csv'

    
