'reinit'

'sdfopen sst_mon_mean.nc'

*Setting the time interval.
year_i = 1981

year_f = 2011

*Initializing the time variable.
year = year_i

m = 1

*Setting the dim. of the row space.
r_dim = 42

*Setting the dim. of the column space.
c_dim = 42

*x-axis domain of the mesh.
x_i = 160

x_f = 270

* y-axis domain of the mesh.
y_i = -10

y_f = 10

*Computing the steps for each axis.
dx = (x_f - x_i)/r_dim

dy = (y_f - y_i)/c_dim

*Configuring the the domain.

'set lat 'y_i%' '%y_f

'set lon 'x_i%' '%x_f

while ( year < year_f )

ym = (year-1891)*12 + m

'set t 'ym

*Initializing the row variable.

i = 1

while (i <= r_dim)

*Intializing the ij-th entry of the matrix.

_aij = ''

*Initializing the column variable.

j = 1

while (j <= c_dim)

*Computing the mean value of the ij-th cell of the mesh.

'd amean(sst, lon= 'x_i + (j - 1)*dx%', lon= '%x_i + j*dx%', lat= '%y_f - i*dy%', lat= '%y_f - (i - 1)*dy%')'

*Taking the result and saving it in a string.

sst = subwrd(result,4)

_aij = _aij%sst

*If the algorithm is working with a column different than the last, adds a ,. 

if(j != c_dim)

_aij = _aij%','

ENDIF

*Pushing the next step in the column.

j = j + 1

ENDWHILE

*If the algorithm if working with the 1-st, then, an existing file will be deleted.

if(i != 1)

matrix=write(''%year%'_'%m%'.csv', _aij, append)

else

matrix=write(''%year%'_'%m%'.csv',_aij)

ENDIF

*Pushing the next step in the row.

i = i + 1

ENDWHILE

*Going to the next year if m = 12.
if(m=12)

year = year + 1

ENDIF 

*Adjusting the month. The counter will restart if m = 12.
if(m < 12)

m = m + 1

else

m = 1

ENDIF

ENDWHILE

;
