# This funcion takes the directory of the EC curves and return
# a data frame and the cardinality of the dataset.
def file2dataset(dir,type):

    import numpy as np
    
    import pandas as pd

    from sklearn.preprocessing import MinMaxScaler

    import os

# Setting the work directory.
    os.chdir(dir)

# Computing the number of files.
    card = len(os.listdir(dir))

# 'raw' refers to no-normalized data.
    if type == 'raw':

# Initializind a dataset frame for the eccs.
        dataset = np.random.rand(1,card,172,2)

# Initializing a counter.
        i = 0

# Going through every file in 'dir'.
        for file in os.listdir(dir):

# Storage the file in the dataset frame.
            dataset[0][i] = pd.read_csv(file,sep=",", header=None)

            i += 1

# Going back to the work directory.
        os.chdir('/home/oscar_amarilla/Nidtec/ML_TDA-ENSO')

# This process refers to the normalization of the y-axis values.
    elif type == 'y-normalized':

# Initializind a dataset frame for the eccs.
        dataset = np.random.rand(card,172)

#Initializing a counter.
        i = 0

# Going trough every file in 'dir'.
        for file in os.listdir(dir):

# Opening the file, normalizing the data and then storing it in the frame.
            ec_y  = pd.read_csv(file,sep=",", header=None)[1]

            dataset[i] = ec_y/ec_y.max()

            i += 1

# Going back to the work directory.
        os.chdir('/home/oscar_amarilla/py_codes')

# 'flatted' refers to taking just the y-axis values.
    elif type == 'flatted':

# Initializind a dataset frame for the eccs.
        dataset = np.random.rand(card,172)

#Initializing a counter.
        i = 0

# Going trough every file in 'dir'.
        for file in os.listdir(dir):

# Opening the file and then storing the data in the frame.
            aux = pd.read_csv(file,sep=",", header=None)

            aux = np.array(aux[:][1])

            dataset[i] = aux.reshape(1, 172)

            i += 1

# Going back to the work directory.
        os.chdir('/home/oscar_amarilla/py_codes')

    return dataset, card
