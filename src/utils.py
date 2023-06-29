import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def events_boundaries(dataset:pd.DataFrame):
    """
    Look for the minimum and/or maximum values of SST anomaly
    in which each phase took palce.

    Parameters
    ----------
    dataset: pd.DataFrame
        a daframe containing historical records of the ENSO 
        phenomena.
    """
    #Looking for the 

    #Netral phase.
    N_lower = dataset['Anomaly (ºC)'][dataset['Phase']==1].min()

    N_upper = dataset['Anomaly (ºC)'][dataset['Phase']==1].max()

    #Niña phase.
    LN_upper = dataset['Anomaly (ºC)'][dataset['Phase']==0].max()

    #Niño phase.
    EN_lower = dataset['Anomaly (ºC)'][dataset['Phase']==2].min()

    print("Neutro interval = [", N_lower, ",", N_upper,"] \nNiña max. =", LN_upper, " \nNiño min. =", EN_lower)

    return [N_lower, N_upper, LN_upper, EN_lower]

def stratifier(database:pd.DataFrame, dataset:pd.DataFrame):
    """
    Reduce the number of neutral events respecting the distribution
    of the events. The events are divided into five classes:
        - ln: Low negative
        - un: Upper negative
        - c: Center
        - lp: Low positive
        - up: Upper positive

    Parameters
    ----------
    database: pd.DataFrame
        a daframe containing the Euler characteristics curve of every
        mean SST field of the database.
    enso_info: pd.DataFrame
        a daframe containing historical records of the ENSO 
        phenomena.

    Returns
    -------
    neutral_index: list
        a list with the indexes of the neutral events.
    dataset_strat: pd.DataFrame
        a dataframe with historical records under the new events distribution.
    neutral_index_strat: list
        a list with the indexes of the neutral events in the new
        distribution.
    database_strat: pd.DataFrame
        a dataframe containing every Euler characteristic curve 
        of the new events distribution. 
    """
    # Taking the index of every neutral event.
    neutral_index = dataset.index[dataset['Phase']==1].tolist()
    # Adding a column where the categories are assigned.
    dataset["cat"]=pd.cut(dataset['Anomaly (ºC)'][neutral_index], bins=5, labels=["ln","un","c","lp","up"])
    cat_index=dataset["cat"][neutral_index]
    # Splitting the database.
    neutro_index,X_test,y_train,y_test=train_test_split(neutral_index, cat_index, test_size=0.41, random_state=0, shuffle=None, stratify=cat_index)
    # Stablishing the new distribution.
    dataset_strat = dataset.drop(index=X_test)
    indexes = database.iloc[X_test].index
    database_strat = database.drop(index=indexes)
    neutral_index_strat = dataset_strat.index[dataset_strat['Phase']==1].tolist()
    return neutral_index, dataset_strat, neutral_index_strat, database_strat

def relabel(enso_info:pd.DataFrame):
    """
    Relabel the neutral events acording to the following criteria
        - Niña: SSTA  ≤  -0.32ºC
        - Neutral: -0.32ºC < SSTA < 0.35ºC
        - Niño: 0.35ºC  ≤  SSTA
    This values SSTA (SST anolmaly) are based in historical records.

    Parameters
    ----------
    enso_info: pd.DataFrame
        a daframe containing historical records of the ENSO 
        phenomena.

    Returns
    ------
    dataset: pd.DataFrame
        the same input data but with changes in the labels of the
        neutral events. 
    """
    dataset = enso_info.copy()
    for i in range(len(dataset)):
        if(dataset['Anomaly (ºC)'][i]<=-0.32):
            dataset.Phase[i]=0
        elif(dataset['Anomaly (ºC)'][i]>-0.32 and dataset['Anomaly (ºC)'][i]<0.35):
            dataset.Phase[i]=1
        elif(dataset['Anomaly (ºC)'][i]>=0.35):
            dataset.Phase[i]=2
    return dataset

def add_labels(enso_info:pd.DataFrame) -> pd.DataFrame:
    dataset = enso_info.copy()
    for i in dataset.index:
        if(dataset['Anomaly (ºC)'][i]<=-0.32 and dataset['Anomaly (ºC)'][i]>-0.92):
            dataset.Phase[i]=1
        elif(dataset['Anomaly (ºC)'][i]>0.35 and dataset['Anomaly (ºC)'][i]<0.91):
            dataset.Phase[i]=3
        elif(dataset['Anomaly (ºC)'][i]>-0.32 and dataset['Anomaly (ºC)'][i]<=0.35):
            dataset.Phase[i]=2
        elif(dataset['Anomaly (ºC)'][i]>=0.91):
            dataset.Phase[i]=4
    return dataset


