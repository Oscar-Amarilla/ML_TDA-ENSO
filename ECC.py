# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 09:30:55 2022

@author: o64am
"""

# importing the required modules.
import numpy as np

import os

import matplotlib.pyplot as plt

#This program will compute the Euler characteristic 
# curve from persistence holomogy data of the SST over 
# the studied region contained in a csv file. The computation will be done
# on every file in a defined directory. Also export plots of every ECC.

#Defining the Euler characteristic function.

def Euler_characteristic(file_name, h):
    
#Initializing the Euler characteristic.

    b_0 = 0

    b_1 = 0

    b_2 = 0
        
#Importing the pesistence homology data.
    with open(file_name, 'r') as data:

#Going through each line.
        for line in data:

#Treating the data of the file.        
            row = np.array(line.split(','))

#Computing the Euler characteristic.
            if (float(row[1]) <= h and float(row[2]) >= h):

#Computing the Betti numbers.
                if(row[0] == '0'):
                    
                    b_0 += 1
                    
                elif(row[0] == '1'):
                        
                    b_1 += 1
                    
                else:
                    
                    b_2 += 1

#Stablishing the Euler characteristic. 
        EC = b_0 - b_1 + b_2
        
    return(EC)

#Settiing the work directory.
os.chdir('/home/oscar_amarilla/Nidtec/ML_TDA-ENSO/Data/Filtration')

dir = r'/home/oscar_amarilla/Nidtec/ML_TDA-ENSO/Data/Filtration'

#Going through every file in "dir".
for x in os.listdir(dir):
    
#Setting the file to be open.
    file_name = str(x)
    
#This line separate the date and the file type.
    aux = np.array(file_name.split('.'))
    
#Initializing the matrix with information about the EC curve.
    ECC = np.zeros((172,2))

#Initializing the height (temperature) parameter.
    h = 14

#Initializing a row counter.
    r = 0
        
#Incresing the height (temperature) til 31.2 degrees.
    while h <= 31.2:
        
#Saving the information of the EC curve.
        ECC[r][0] = h
        
        ECC[r][1] = Euler_characteristic(file_name, h)
            
#Increasing step.
        h = h + 0.1
        
#Pushing to next row in the ECC matrix.
        r = r + 1
            
            #print(h)
    x = ECC[:, 0]
    
    y = ECC[:, 1]

#Naming the plot
    fig = plt.figure()
#Plotting the points 
    plt.plot(x, y)
    
#Naming the x axis
    plt.xlabel('Temperature')
#Naming the y axis
    plt.ylabel('Euler characteristic')
    
#Graph title.
    graph_name = aux[0] + ' Euler characteristic curve'
  
#Giving a title to the graph.
    plt.title(graph_name)
  
#Saving the plot.
    plt.savefig('/home/oscar_amarilla/Nidtec/ML_TDA-ENSO/Data/EC_curves/' + aux[0] + '.png', dpi = 200)
    
#Function to show the plot
#    plt.show()    

#Setting the output directory.
    dir_out = '/home/oscar_amarilla/Nidtec/ML_TDA-ENSO/Data/ECC/' + file_name

#Saving the file.
    np.savetxt(dir_out, ECC[:,1], delimiter= ",", fmt='%.1f')

# Close the 
    plt.close(fig)
