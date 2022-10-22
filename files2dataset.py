# This funcion takes the directory of the EC curves and return
# a data frame of 1xcard dimension. Also return the cardinality 
# of the dataset.
def file2dataset(dir,type):

    import numpy as np
    
    import pandas as pd

    import os

# Setting the work directory.
    os.chdir(dir)

# Computing the number of files.
    card = len(os.listdir(dir))

    if type == 'classifier':

    # Initializind a dataset for the eccs.
        dataset = np.random.rand(1,card,172,2)

    #Initializing a counter.
        i = 0

    # Going trough every file in 'dir'.
        for file in os.listdir(dir):

    # Open the file.
            dataset[0][i] = pd.read_csv(file,sep=",", header=None)

            i += 1

    # Setting the work directory.
        os.chdir('/home/oscar_amarilla/Nidtec/ML_TDA-ENSO')

    if type == 'lgstcRgrssn':

    # Initializind a dataset for the eccs.
        dataset = np.random.rand(card,172)

    #Initializing a counter.
        i = 0

    # Going trough every file in 'dir'.
        for file in os.listdir(dir):

    # Open the file.
            aux = pd.read_csv(file,sep=",", header=None)

            aux = np.array(aux[:][1])

            dataset[i] = aux.reshape(1, 172)

            i += 1

    # Setting the work directory.
        os.chdir('/home/oscar_amarilla/py_codes')



    return dataset, card
