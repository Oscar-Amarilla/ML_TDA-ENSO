'''This algorithm related a trimester of the ENSO with the corresponding months.

Here, every phase is represeted by a number:
    Neutro -> 0
    La Niña -> 1
    El Niño -> 2
'''

import numpy as np

def oni2month(phases):

    enso_month=np.zeros(len(phases)+2, int)

    for i in range(0, len(phases)):

        if i == 0:

            enso_month[i] = 1

        #    if phases[i] == 'Neutro':

         #       for j in range(0,3):

          #          enso_month[i+j] = 0

           # elif phases[i] == 'La Niña':

            #    for j in range(0,3):

             #       enso_month[i+j] = 1

            #else:

               # for j in range(0,3):

                #    enso_month[i+j] = 2
        else:

            if phases[i] == 'Neutro':
                
                enso_month[i] = 0

            elif phases[i] == 'La Niña':

                    enso_month[i] = 1

            else:

                    enso_month[i] = 2

    return  enso_month





