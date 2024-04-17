library("TDA")
filtration <- function(temp_field){
# This program extract topological information and export persistence 
# homology of the processes field.
# 
# Parameters
# ----------
# temp_field: matrix
#   a matrix containing the mean SST distribution of the study region.
#
# Returns
# -------
# DiagGrid: list
#   a list with the sublevel filtration data.

    sst <- as.matrix(temp_field)
# Creating a mesh for the process
    Xlim <- c(1, 22) 
    Ylim <- c(1, 110)
    Tlim <- c(0,40)
    by <- 1
    Xseq <- seq(Xlim[1], Xlim[2], by = by)
    Yseq <- seq(Ylim[1], Ylim[2], by = by)
    Tseq <- seq(Tlim[1], Tlim[2], by = by)
    Grid <- expand.grid(Xseq, Yseq, Tseq)    
# Doing the filtration.
    DiagGrid <- gridDiag(
      X = NULL, FUN = NULL, lim = NULL, by = NULL, FUNvalues = sst, maxdimension = 2,
      sublevel = TRUE, library = "GUDHI", location = FALSE,
      printProgress = FALSE)
    return(DiagGrid)
}
