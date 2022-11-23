
def oni(means):
    ''' This function determine if a three month mean correspond to
    a neutral, cold or warm phase of the ENSO.
    '''
# Initializing the array containg the ENSO phase. 
    enso_phase = []
# Initializing a counter. This counter is part of the criteria for 
# determine which phase is running in a moment of time.
    counter = 0
# Auxiliar variable showing the current work line.
    place = 0
    
# Going through the monthly anomaly.
    for mean in means:

# Determining a warm phase.
        if mean >= 0.5:

            counter = counter + 1
# If the last five trimestres were above the 0.5 temperature
# anomaly, a warm phase is declared.
            if counter >= 5:

# Setting the actual place as a warm phase.
                enso_phase.append('El Niño')

# Declaring the last 4 trimestres as part of the warm phase.            
                for i in range(1,5):

                    enso_phase[place - i] = 'El Niño'

            else:  
# Declaring neutral phase; conditions weren't achived.  
                enso_phase.append('Neutro')

# Determining a warm phase.
        elif mean <= -0.5:

            counter = counter + 1


# If the last five trimestres were below the -0.5 temperature
# anomaly, a cold phase is declared.
            if counter >= 5:
                
# Setting the actual place as a cold phase.
                enso_phase.append('La Niña')

# Declaring the last 4 trimestres as part of the cold phase.            
                for i in range(1,5):

                    enso_phase[place - i] = 'La Niña'

# Declaring neutral phase; conditions weren't achived.  
            else:  
    
                enso_phase.append('Neutro')
        
        else:  
    
            counter = 0

            enso_phase.append('Neutro')

# Moving to the next line.
        place = place + 1
    
    return   enso_phase

