import numpy as np

import pandas as pd

import csv

from oni import oni

from oni2month_num import oni2month

#from mise_en_place import mise_en_place

# Initializing the data storage.
means = [1.5] 

# Importing the data and putting the raw data ready to use.

file_dir = '/home/oscar_amarilla/Nidtec/ML_TDA-ENSO/Data/month_oni_data.csv'

data = pd.read_csv(file_dir, header=None, sep=',')

data.columns=['Year','Month', 'Anomaly']

# Computing the mean values.
for i in range(1,len(data)):

    if data['Year'][i] < 2022:

        mean = round((data['Anomaly'][i - 1] + data['Anomaly'][i] + data['Anomaly'][i + 1])/3, 1)

        means.append(mean)
        
# Using the ONI criteria.
oni = oni(means)

# Matching every month with its trimestrer under the ONI criteria.
phases = oni2month(oni)

# Adjusting the dimensions of the dataframe. 
data = data.drop(data.index[len(phases):len(data)])

# Adding a fourth column to the input data about the ENSO phases.
data['ONI'] = phases

output = data

#Setting the output directory.
dir_out = '/home/oscar_amarilla/Nidtec/ML_TDA-ENSO/Data/ENSO.csv'

output.to_csv(dir_out, header=None, index=None)

# open the file in the write mode.
#f = open(dir_out, 'w')

# create the csv writer.
#writer = csv.writer(f)

# write outpur into a csv file.
#writer.writerows(output)

# close the file.
#f.close()
