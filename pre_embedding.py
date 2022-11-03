def pre_embedding(dataset):
    
    import numpy as np
   
    dataset = dataset.astype(int)

    coeff = np.array([0])
    
    for ecc in dataset:
    
        for t in ecc:
        
            for c  in coeff:
            
                if t != c:
                
                    counter += 1
                
                else:
                
                    counter = 0
                    
                    break

            if counter != 0:

                coeff = np.append(coeff, t)

    coeff.astype(int)

    dataset_out = np.random.rand(864, 172)

    j = 0

    for ecc in dataset:

        i = 0

        linear_comb= np.zeros(172)

        for t in ecc:

            for c in coeff:

                if t == c:

                    linear_comb[i] = coeff.tolist().index(c)

            i +=1

        dataset_out[j] = linear_comb

        j +=1

    return coeff,dataset_out.astype(int)



    



