def features_extraction(dataframe):

    import tsfresh

    import anomalous

    import pandas as pd

    features_dataframe = pd.DataFrame(columns=["Mean", "Variance","Nº peaks", "Entropy"])

    for i in range(0,864):

        mean=tsfresh.feature_extraction.feature_calculators.mean(dataframe[i])

        variance=tsfresh.feature_extraction.feature_calculators.variance(dataframe[i])

        peaks=tsfresh.feature_extraction.feature_calculators.number_peaks(dataframe[i],2) 

       # trend=tsfresh.feature_extraction.feature_calculators.linear_trend(dataframe[i],1)

        entropy=tsfresh.feature_extraction.feature_calculators.sample_entropy(dataframe[i])

        features_dataframe=features_dataframe.append({'Mean':mean, 'Variance':variance, 'Nº peaks':peaks, 'Entropy':entropy},ignore_index=True)
    
    pd.DataFrame(features_dataframe)

    y = anomalous.ts_measures(dataframe)

    # Putting all the information in one dataframe.
    
    y[list(features_dataframe)] = features_dataframe
    
    del y["KLscore"]
    
    del y["change_idx"]
    
    del y["variable"]
    
    features_dataframe = y

    return features_dataframe 
