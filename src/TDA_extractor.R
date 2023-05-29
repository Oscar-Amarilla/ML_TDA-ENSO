#This program extract topological information and export persistence diagrams, barcodes
# and csv files with the persistence information. The csv files are aimed to be 
# processed by ECC.py to get the Euler characteric curve of each of them.

# Importing the TDA library.
library("TDA")

filtration <- function(temp_field){

#Setting the file name.
    sst <- as.matrix(temp_field)
   
# Creating a mesh for the plot.
    Xlim <- c(1, 22) 
    Ylim <- c(1, 110)
    Tlim <- c(0,40)
    by <- 1
    Xseq <- seq(Xlim[1], Xlim[2], by = by)
    Yseq <- seq(Ylim[1], Ylim[2], by = by)
    Tseq <- seq(Tlim[1], Tlim[2], by = by)
    Grid <- expand.grid(Xseq, Yseq, Tseq)
    
# Making the diagrams.
    DiagGrid <- gridDiag(
      X = NULL, FUN = NULL, lim = NULL, by = NULL, FUNvalues = sst, maxdimension = 2,
      sublevel = TRUE, library = "GUDHI", location = FALSE,
      printProgress = FALSE)
    
# Printing the topological data.
    return(DiagGrid)
    
#   holder <- paste(year,month,sep='_')

# Importing the filtration data.
#    file_name <- paste("outputs/filtration/", holder, ".txt", sep="")
#    cat(capture.output(print(DiagGrid), file=file_name))
}
