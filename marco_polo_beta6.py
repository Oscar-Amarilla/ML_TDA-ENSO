# This algorithm use a LSTM model with cross validation for classify the ECC.
from sklearn.model_selection import KFold

from portion import portion

from files2dataset import file2dataset

from pre_embedding import pre_embedding

import tensorflow as tf

from tensorflow.keras.models import Sequential

from tensorflow.keras.layers import LSTM, Dense, Embedding

from tensorflow.keras import datasets

import pandas as pd

import numpy as np

import os

# ECC files diretory.
dir = '/home/oscar_amarilla/Nidtec/ML_TDA-ENSO/Data/ECC/'

dataset, card = file2dataset(dir, 'y-normalized')

coeff, dataset = pre_embedding(dataset)

# Partitioning the data.
prtn = portion(80, card)

# Importing the data.
enso_file = '/home/oscar_amarilla/Nidtec/ML_TDA-ENSO/Data/ENSO.csv'

# Praparing the data.
enso_info=pd.read_csv(enso_file,sep=",", header=None)

enso_label=enso_info[:864][3]

train_ecc = dataset[0:prtn]

train_label = np.array(enso_label[0:prtn])

test_ecc = dataset[prtn:]

test_label = np.array(enso_label[prtn:])

# Assembling the model.
model = Sequential([

#Embedding(172, 3, input_length=172),
Embedding(len(coeff), 2, input_length=172),

# The model consist of 16 LSTM units that process 172x2 matrices.
LSTM(units=8),

# The model output is a probabilty distribution of 3 possible cases. 
# The raw output pass through softmax.
    Dense(3,activation='softmax'),

    ])

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

history = model.fit(train_ecc, train_label , epochs=5, validation_data =(test_ecc, test_label))

# Printing in screen the structure of the model.
model.summary()

predictions = model.predict(test_ecc)
