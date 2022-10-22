# This algorithm use a LSTM model with cross validation for classify the ECC.
from sklearn.model_selection import KFold

from portion import portion

from files2dataset import file2dataset

import tensorflow as tf

from tensorflow.keras.models import Sequential

from tensorflow.keras.layers import LSTM, Dense

from tensorflow.keras import datasets

import pandas as pd

import numpy as np

import os

# Avoinding warnings in the screen.
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

# Assembling the model.
model = Sequential([

# The model consist of 16 LSTM units that process 172x2 matrices.
    LSTM(16, input_shape=(172,2)),

# The model output is a probabilty distribution of 3 possible cases. 
# The raw output pass through softmax.
    Dense(3,activation='softmax'),

    ])

# Printing in screen the structure of the model.
model.summary()

# Setting an optimizer for the model.
optimizer=tf.keras.optimizers.Adam(lr=0.01)

# Batching the dataset.
batch_size=4

# Setting a loss function for the model.
loss='SparseCategoricalCrossentropy'

# Setting a messurment of the model performance.
metrics=['accuracy']

# Compiling the model.
model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

# Starting the cross validation.
kf = KFold(n_splits=4) 

# Initializing cross validation variables.
fold= 0

# ECC files diretory.
dir = '/home/oscar_amarilla/Nidtec/ML_TDA-ENSO/Data/ECC/'

dataset, card = file2dataset(dir, 'classifier')

# Partitioning the data.
prtn = portion(80, card)

# Importing the data.
enso_file = '/home/oscar_amarilla/Nidtec/ML_TDA-ENSO/Data/ENSO.csv'

# Praparing the data.
enso_info=pd.read_csv(enso_file,sep=",", header=None)

enso_label=enso_info[31*12:732][3]

train_ecc = dataset[0][0:prtn]

train_label = np.array(enso_label[0:prtn])

test_ecc = dataset[0][prtn:]

test_label = np.array(enso_label[prtn:])

for train, test in kf.split(train_label):

    fold +=1

    print("Fold %", fold)

    ecc_folded = train_ecc[train]

    label_folded = train_label[train]
    
    ecc_test = train_ecc[test]

    label_test = train_label[test]
    
    history = model.fit(ecc_folded, label_folded, batch_size=batch_size, epochs=5, validation_data =(ecc_test, label_test))

predictions = model.predict(test_ecc)
