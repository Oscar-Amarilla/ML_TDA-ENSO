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

# Assembling the model.
model = Sequential([

# The model consist of 16 LSTM units that process 172x2 matrices.
LSTM(16, input_shape=(172,2)),

    Dense(8,activation='tanh'),

# The model output is a probabilty distribution of 3 possible cases. 
# The raw output pass through softmax.
    Dense(3,activation='softmax'),
    
    ])

# Printing in screen the structure of the model.
model.summary()

# Setting an optimizer for the model.
optimizer=tf.keras.optimizers.Adam(lr=0.004)

# Batching the dataset.
batch_size=16

# Setting a loss function for the model.
loss='SparseCategoricalCrossentropy'

# Setting a messurment of the model performance.
metrics=['accuracy']

# Compiling the model.
model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

# ECC files diretory.
dir = '/home/oscar_amarilla/Nidtec/ML_TDA-ENSO/Data/ECC/'

dataset, card = file2dataset(dir, 'y-normalized')

# Partitioning the data.
prtn = portion(80, card)

# Importing the labels.
enso_file = '/home/oscar_amarilla/Nidtec/ML_TDA-ENSO/Data/ENSO.csv'

# Praparing the data for the process.
enso_info=pd.read_csv(enso_file,sep=",", header=None)

enso_label=enso_info[:][3]

train_ecc = dataset[0][0:prtn]

ecc_l = len(train_ecc)

train_label = np.array(enso_label[0:prtn])

lbl_l = len(train_label)

test_ecc = dataset[0][prtn:]

test_label = np.array(enso_label[prtn:])

# Appling the moving window cross validation method.
for x in range(0,8):

    prcnt = (x + 2)*10

    print("Percentage of data used: ", prcnt)

    ecc_nfold = train_ecc[int(x/10*ecc_l):int((x+2)/10*ecc_l)]

    label_nfold = train_label[int(x/10*lbl_l):int((x+2)/10*lbl_l)]

    ecc_test = train_ecc[int((x+2)/10*ecc_l):int((x+3)/10*ecc_l)]

    label_test = train_label[int((x+2)/10*lbl_l):int((x+3)/10*lbl_l)]

# Fitting the model.
    history = model.fit(ecc_nfold, label_nfold, epochs=5, validation_data =(ecc_test, label_test))

# Making predictions.
predictions = model.predict(test_ecc)
