def phase_probability(km_output):

    km_output_0 = 0
    
    km_output_1 = 0
    
    km_output_2 = 0

    for i in range(len(km_output)):

        if km_output[i] == 0:

            km_output_0 += 1

        elif km_output[i] == 1:

            km_output_1 += 1

        else:

            km_output_2 += 1

    probabilities = [ round(km_output_0*100/len(km_output)), round(km_output_1*100/len(km_output)), round(km_output_2*100/len(km_output))]

    print("Probability of neutral phase: " + str(probabilities[0]) + " %")
        
    print("Probability of Ninha  phase: " +  str(probabilities[1]) + " %")
        
    print("Probability of Ninho phase: " + str(probabilities[2]) + " %")

    return probabilities
