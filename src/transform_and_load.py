import numpy as np
import pandas as pd
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri
from typing import Tuple
import netCDF4 as nc
import math
import os

##------------------------- Auxiliary functions ----------------------------------
def year_month_num(year:int,month:int) ->int:
    """
    Take a year and a month and return a number from 0 "Jan 1891" to 
    1577 (May 2022)  

    Parameters
    ----------
    year:int
        year of interest
    month:int
        month of interest

    Returns
    -------
        number of months since Jan 1891 : int
    """
    return (year-1891)*12 + month-1

def get_extremes(temp_field:np.array, lower_temp:float=56.7, higher_temp:float=-273.15)->Tuple[float,float]:
    """
    Takes the maximum and minimun meassure of temperature of a 
    temperature field.  

    Parameters
    ----------
    temp_field:np.array
        an n dimensional NumPy array with temperature measures.
     -- Initialization parameters --
    lower_temp:float
        lowest temperature estimate.
    higher_temp:float
        higher temperature estimate.

    Returns
    -------
        lower_temp:float
            lowest temperature in the record.
        higher_temp:float
            higher temperature in the record.
    """
    max_temp = temp_field.max()
    min_temp = temp_field.min()
    if max_temp > higher_temp:
        higher_temp = max_temp
    if min_temp < lower_temp:
        lower_temp = min_temp
    return math.floor(lower_temp), math.ceil(higher_temp)

##------------------------- TDA block ----------------------------------
def filtration(temp_field:np.array) -> np.array:
    """
    Performs the sub-level filtrarion  of the input. The filtration 
    is done by the TDA_extractor script, which is written in R 
    languge. The execution of the R code in a Python environmenr is
    posible thanks to the rpy2 package. 

    Parameters
    ----------
    temp_field:np.array
        an n dimensional array with temperature measures.

    Returns
    -------
        np_filt_data: np.array
            Ouput of the filtration (R) function.
    """
    # Allowing the presence of R object in the Python environment.
    rpy2.robjects.numpy2ri.activate()
    # Loading the R script.
    with open('src/TDA_extractor.R') as f:
        code = f.read()
    # Turning the script in an R object.
    robjects.r(code)
    # Turning a n-dimensional NumPy array into a R matrix.
    r_matrix = robjects.r.matrix(temp_field,nrow=temp_field.shape[0],ncol=temp_field.shape[1])
    # Applying the "filtration" function on the R matrix and then turning the 
    # output into a NumPy array. 
    np_filt_data = np.array(
        robjects.r['filtration'](r_matrix))[0]
    return np_filt_data

def Euler_characteristic(filtration:np.array,level:float):
    """
    Computes the Euler characteristic a simplicial subcomplex
    based on the sublevel filtration output.

    Parameters
    ----------
    filtration:np.array
        an array with three columns, cotaining a particular Betti 
        number, its birth and its death.
    level:float
        current value of the height function.

    Returns
    -------
        Euler characteristic: int
            output of the Euler-Poncare theorem.
    """
    #Initializing the Betti numbers.
    b_0 = 0
    b_1 = 0
    b_2 = 0

    for i in range(filtration.shape[0]):
        # Getting the Betti numbers of the current level.    
        if (filtration[i][1] <= level and filtration[i][2] >= level):
            if(filtration[i][0] == 0):
                b_0 += 1
            elif(filtration[i][0] == 1):
                b_1 += 1
            else:
                b_2 += 1

    # Computing the Euler characteristic (Euler-Pointcare formula).
    return b_0 - b_1 + b_2

def ECC(filtration:np.array, h_0:float, h_f:float) -> np.array:
    """
    Computes the Euler characteristic curve of a simplicial complex
    based on the sublevel filtration output. The curve will be computed 
    with an increse in height/temperature of 0.1ºC in each iteration.

    Parameters
    ----------
    filtration:np.array
        an array with three columns, cotaining a particular Betti 
        number, its birth and its death.
    h_0:float
        point where the height value is 0.
    h_f:float
        upper bound of the height function domain (-inf,h_f].

    Returns
    -------
        ecc: np.array
            Euler characteristic of each subcomplex taken.
    """
    # Initializing a NumPy array with information about the EC curve.
    num_steps = int((h_f-h_0)/0.1)
    ecc = np.zeros(num_steps)
    for r in range(num_steps):
    # Saving the information of the EC curve.
        level = h_0 + r*0.1
        ecc[r] = Euler_characteristic(filtration, level)
    return ecc

def TDA_process(sst:nc._netCDF4.Dataset)->pd.DataFrame:
    """
    This function has two parts. The first get the extremes values of 
    the temperature fields in the period of interest, and the second 
    takes each temperature field, apply the sublevel filtration to them
    and then computes the Euler characteristic curve of each. Every 
    curve is stored in a Pandas dataframe.

    Parameters
    ----------
    sst:netCDF4
        a database containing the global monthly mean sea surface 
        temperature from Jan 1891 to May 2022.
    Returns
    -------
    database:pd.DataFrame
        a dataframe containing every Euler characteristic curve. 
    """
    lower_temp= 56.7 
    higher_temp= -273.15
    for year in range(1950,2022):
        for month in range(1,13):
            # Turning a month-year date into a number from 0 to len(data_time_domain).
            date_num = year_month_num(year,month)
            # Getting the mean sst field of the region of study at a particular date.
            temp_field = np.array(sst[date_num,79:101,160:270])
            # Searching for the extremes.
            lower_temp, higher_temp = get_extremes(temp_field,lower_temp,higher_temp)
    
    # Initializing the daframe database.
    col_dim = int((higher_temp-lower_temp)/0.1)
    database = pd.DataFrame(columns=list(range(col_dim)))
    for year in range(1950,2022):
        for month in range(1,13):
            date_num = year_month_num(year,month)
            temp_field = np.array(sst[date_num,79:101,160:270])
            # Applying TDA.
            filt_data = filtration(temp_field)
            # Stablishing an index for output data into the dataframe.
            index = str(year) + '_' + str(month)
            database.loc[index] = ECC(filt_data,lower_temp,higher_temp)
    return database

##----------------------- ENSO block -------------------------------

def phase_id(means:list):
    """
    Receives an array containing the quarterly moving average of the 
    study period and applies the ONI criteria to define the ENSO phase
    of each month. If a quarter is declared as a particular phase, then 

    ONI criteria:
     If the quarterly moving average of the anomaly in the SST of the
     Niño 3.4 region in absolute value is greter than 0.5ºC for five 
     consecutive moving quarters, then it is declase a
     - Niña phase: if the anomaly is negative,
     - Niño phase: if the anomaly is positive.
     Otherwise, normal conditions (Neutral phase) are running.

      

    Parameters
    ----------
    means:list
        a list containing quarterly moving averages.
    Returns
    -------
    database:pd.DataFrame
        a dataframe containing every Euler characteristic curve. 
    """
    enso_phase = []*len(means)
# Initializing a counter. This counter is part of the criteria for 
# determine which phase is running in a moment of time.
    counter = 0
# Going through the monthly anomaly.
    for i,mean in enumerate(means):
# Determining a warm phase.
        if mean >= 0.5:
            counter += 1
# If the last five trimestres were above the 0.5 temperature
# anomaly, a warm phase is declared.
            if counter >= 5:
# Setting the actual place as a warm phase.
                enso_phase.append(2)
# Declaring the last 4 trimestres as part of the warm phase.            
                for j in range(1,5):
                    enso_phase[i-j] = 2
            else:  
# Declaring neutral phase; conditions weren't achived.  
                enso_phase.append(1)
# Determining a warm phase.
        elif mean <= -0.5:
            counter += 1
# If the last five trimestres were below the -0.5 temperature
# anomaly, a cold phase is declared.
            if counter >= 5:
# Setting the actual place as a cold phase.
                enso_phase.append(0)
# Declaring the last 4 trimestres as part of the cold phase.            
                for j in range(1,5):
                    enso_phase[i-j] = 0
# Declaring neutral phase; conditions weren't achived.  
            else:  
                enso_phase.append(1)
        else:  
            counter = 0
            enso_phase.append(1)
    
    return enso_phase

def ONI(data:pd.DataFrame) -> pd.DataFrame:
    # Initializing the mean value array.
    means = [1.5] 
    # Computing the mean values.
    for i in range(1,len(data)):
        if data['Year'][i] < 2022:
            mean = round((data['Anomaly (ºC)'][i - 1] + data['Anomaly (ºC)'][i] + data['Anomaly (ºC)'][i + 1])/3, 1)
            means.append(mean)
            
    # Appliying the ONI criteria and matching every month with its trimestrer under the ONI criteria.
    phases = phase_id(means)
    # Adjusting the dimensions of the dataframe. 
    data = data.drop(data.index[len(phases):len(data)])
    # Adding a fourth column to the input data about the ENSO phases.
    data['Phase'] = phases
    return data
