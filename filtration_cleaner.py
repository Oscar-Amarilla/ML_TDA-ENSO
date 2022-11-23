# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 10:56:53 2022

@author: o64am
"""

"""This algorithm take out the headers of the filtrations files fron
the Filtration_raw directory."""

import numpy as np

import os

#Settiing the work directory.
os.chdir('/home/oscar_amarilla/Nidtec/Filtration_raw/')

dir = r'/home/oscar_amarilla/Nidtec/Filtration_raw/'

#Going through every file in "dir".
for x in os.listdir(dir):
    
    file_name = str(x)
    
#Initializing the matrix with homological information.
    homology_matrix = []
    
#Importing the sst matix data.
    with open(x, 'r') as data:
        
        print(x)
    
        switch = 0
    
        for line in data:
        
            row = line.split()
        
            if (switch > 1 and len(row) != 0):
        
                homology_matrix.append(row[1:4])
        
            else:
        
                switch = switch + 1 
                
        #print(homology_matrix)
    
#Setting the output directory
    dir_out = '/home/oscar_amarilla/Nidtec/Filtration/' + file_name

    np.savetxt(dir_out, homology_matrix, delimiter= ",", fmt='%s')

        
        


