------------------FIRST ORDER SCRIPTS-------------------------------

-> SST2matrix.gs: An openGrads script that grid the domain and take the 
mean temperature value of each cell. The output is stored in SST_monthly
folder.

-> TDA_extractor.R: An R script using the TDA CRAN package to obtain 
topological data form each sst field. The data obteined are the 
barcode plots and the low level filtration diagrams. The output
is stored in the Barcode,Filtration_raw and Diagram folders.

-> Filtration_cleaner.py: A short script for take out the headers 
of the filtrations files in the Filtration_raw folder. The output 
goes to the Filtration folder.

-> ECC.py: Takes the filtrations from Filtration folder and compute the Euler 
characteristic cureves. The output goes to ECC and EC_curves.

-> id_enso.py: This script take the month_oni_data.csv file and generates the
ENSO label phases with respect to the ONI criteria. The labels follows the 
following form:

[0]: Neutral phase, [1]: Niña phase, [2]: Niño phase.

The output is in the fourth column of the ENSO.csv.

-> Clustering.ipynb: A Jupyter Notebook wich apply clusterization to the 
Euler characteristic curves.

------------------AUXILIARY SCRIPTS-------------------------------

-> oni2month_num.py: A script used by id_enso.py to label each month 
with its corresponding ENSO phase.

-> mise_en_place.py: Arrange the input data for the id_enso.py script
and then add the fourth column to the output file.

-> files2dataset.py: Take an Ecc and return it as a dataset of 172x2 matrix
 (coordinates) or a 172 length array (only y values).

-> portion.py: Used in the Clustering script to partitioning the data.

-> matching_beta.py: It coumputes the difference between a labeled Ecc and
the clustered Eccs.
