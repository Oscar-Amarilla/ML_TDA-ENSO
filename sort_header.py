import numpy as np

def sort_header(header):

   header.sort()

   for i in range(len(header)-1):

       for j in range(i+1,len(header)):

           if header[i].split("_")[0] == header[j].split("_")[0]:

               a = int(header[i].split("_")[1])

               b = int(header[j].split("_")[1])

               if a > b: 

                   aux = header[j]

                   header[j] = header[i]

                   header[i] = aux

#       else:

 #           print("Go fuck yourself.")

   return header
