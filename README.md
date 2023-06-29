# [ML_TDA-ENSO](https://github.com/Oscar-Amarilla/ML_TDA-ENSO)

by Oscar Amarilla, 2023

[ML_TDA-ENSO](https://github.com/Oscar-Amarilla/ML_TDA-ENSO) stands for *Machine Learning*, *Topological Data Analysis* and *El Niño-South Oscillation*, which are topics covered in this academic work. This porject will be presented by the main author as undergraduate thesis to obtain a degree in Atmospheric Sciences at the National University of Asunción (Paraguay). This project has been developed at the [Scientific Computing and Applied Mathematics](https://nidtec.pol.una.py/ccyma/) group at the [NIDTEC](https://nidtec.pol.una.py/) research center of the same university.

## Authors

- [Oscar Amarilla](https://www.linkedin.com/in/oscar-amarilla/) ¹ (Main author)
- [Cristhian Schaerer](https://www.linkedin.com/in/christian-schaerer-bb4440238/)¹ (Advisor and contributor)
- [Inocencio Ortiz](https://www.linkedin.com/in/ino-ortiz-101317/)² (Advisor and contributor)</br>

¹National University of Asunción, Polytechnic School, San Lorenzo, Paraguay.</br>
²National University of Asunción, Faculty of Engineering, San Lorenzo, Paraguay.

The user is free to copy, modify, and distribute this proyect, even for commercial purposes under the Creative Commons Attribution 4.0 International Public License. See *[license dedication](#license)* for details.

## Table of Contents
1. [About](#about)
2. [El Niño-Southern Oscillation](#el-niño-southern-oscillation)
3. [Topological Data Analysis](#topological-data-analysis)
4. [Support Vector Machine](#support-vector-machine)
5. [Dependencies](#dependencies)
6. [Installation](#installation)
7. [Structure of the Project](#structure-of-the-project)
9. [Future Work](#future-work)
10. [References](#references)
11. [Contributing to ML_TDA-ENSO](#contributing-to-ml_tda-enso)
12. [License](#license)

## About

In this project the mean monthly sea surface temperature fields of the topical Pacific region defined by (10°N-10°S,160°E-90°O) of each month in the period 1950-2021 are taken and topological data analysis is applied on them. This process consists in computing the sublevel set filtration and the Euler characteristic curve of each field. Then, this curves are given as input data to a support vector machine algorithm to verify if the data set is linearly separable.

The aim is to develop a classifier of ENSO phases based on topological data.

## El Niño-Southern Oscillation
El Niño-Southern Oscillation (ENSO) is an irregular oscillation with periods in the range of two to seven years that alters the normal conditions of the atmosphere of the central tropical Pacific. It consists in a warm phase (El Niño), a cold phase (La Niña) and a neutral phase (normal conditions). Depending in which of phases of the extrmees phases it is active, its manifestation implies anomalies in the amount of rainfall in the regions bordering the Pacific, opening the possiblily of periods of droughts or floods[1][2].

The National Oceanic and Atmospheric Administration (NOAA) monitors the current state of the phenomena with an index developed exclusively for this purpose called the Oceanic Niño Index (ONI). The ONI statablishes that if the absolute value of  the anomaly of the running quarterly average of the sea surface temperature (SST) of the Niño 3.4 region (5ºN - 5ºS, 120º - 170ºO) with respect to 30-year average updated every 5 years is greater than 0.5ºC for 5 consecutive overlaping three-month periods, the normal conditions are broken. If the anomaly is negative, a Niña phase is running, and if it is positive, is a Niño phase[4]. 

## Topological Data Analysis

### Simplicials and simplicial complexes

Topological Data Analysis (TDA) is a branch of applied mathematics based on algebraic topology that look after trends and structures in the underlying topology of a particular dataset. The core of TDA is the "simplex", wich is an geometric element that conect data poits in its particular ambience. Simplices are setted by order:
<ul>
    <li>0-dimensional: a vertex (point),</li>
    <li>1-dimensional: a line segment,</li>
    <li>2-dimensional: a triangle (surface),</li>
    <li>3-dimensional: a tetrahedron,</li>
</ul>

and so on. Every $n$-dimensional simplex, with $n \geq 1$, has as faces (borders) a set of  ($n-1$)-dimensional simpleces. This relationship is captured by a mathematical function called <em>boundary map</em>.

### Homology group and Betti number

Let $\phi$ be a $k$-dimensional simplex and $\tau_i$ one of it faces, then the boundary map $\partial_k$ 
$$\partial_k(\phi) = \sum_i^n(-1)^i\tau_i$$
maps $\phi$ to the formal sum of its faces.

A very interesting output from $\partial_k$ is that the composition $\partial_{k-1} \circ \partial_k$ maps to zero. Two simplices can join only along one of its faces of the same dimension. When many simplices are joined, the set $X$ of simplices is called a <em>simplicial complex</em>. 

Some of this joined simplicials can configure an $n$-dimensional voids, and one of the purposes of TDA is dicern voids from sum of faces. This can be achived by taking a look to those arguments that $\partial_k$ maps to zero. Those formal sums that actually represent the boundary of a $(k+1)$-dimensional simplex will be placed in the set $B_k(X)=Im(\partial_{k+1})$, on the other hand, all the formal sums that $\partial_k$ maps to zero, typically called <em>loops</em>, are elements of the set $Z_k(X)=Null(\partial_k)$. Something not hard to realize is that $B_k \subseteq Z_k$.

Finally, the formal sums that strictly are $k$-dimensional voids in the simplicial complex are elements of the set

$$H_k = B_k/Z_k$$

called <em>hology group</em>. Then, the dimension of $H_k$ is called $k$-Betti number, denoted by $\beta_k$, represents the number of $k$-dimensional voids in a simplicial complex. In the case of $k=0$, the results are related to the connected components in $X$.  

### Sublevel filtration

Filtration is a technique used to compute something called <em>persistent homology</em>, which is a way to track the topological features at different scales. There are different approaches of this technique, in this work will be applied a <em>sublevel set filtration</em>.

In a more formal way, a filtration is a sequence of neasted subcomplexes 

$$\emptyset \subseteq X_0 \subseteq X_1 \subseteq ... \subseteq X_n = X$$

where the homology group is computed in each $X_i$. When a topological features appears in a subcomplex $X_i$ and disappear in $X_j$, its said that the feature born in $i$ and dies in $j$. How to go from $i$ to $j$ depends in how simplicials are builded.

In a sublevel set filtration, the simplicial complex is already given. Here, one go from $i$ to $j$ by a <em>height function</em> $f:X \rightarrow \mathbb{R}$, which maps a vertex in $X$ to the height of it with respect to a plane on which $X$ rest. 

### Euler characteristics curve

The Euler characteristic is a conpcept from the study of polyhedras that is bringed to topology, adapted and ended up being a topological invariant. In topology, it is an integer  number that results of the alter sum af the Betti number of a simplicial complex $X$ with dimension $|X|$ 

$$\text{\large $\chi$}(X) = \sum_{i=0}^{|X|}(-1)^i\beta_i .$$

being $|X|$ equal to the dimension of higher simplex in the complex.

The Euler characteristic curve induced by the height function is a continuous map 

$$	\begin{array}{lll} E : & \mathbb{R} \rightarrow \mathbb{Z} \\ &  a \mapsto \text{\large $\chi$}(X_a)\end{array}$$

that computes the Euler characteristics of each subcomplex⁷. 

## Support Vector Machine

Support vector machine (SVM) is a machine learning algorithm that takes a set of data $S$ and generate an hyperplane that separates the data in two regions for binary classification⁸. It can be applied also for multinomial classification by techniques like <em>one vs the rest</em>, a binary classification where one class it separated from the rest⁹.

Sometimes data is not </em>linearly separable</em>, for this cases a technique was developed that envolves a special type of non-linear functions called <em>kernels</em>. This functions map the data to another enviorment with different dimension, tipically higher, where the data can be separable with an hyperplane⁸.  

## Dependencies

This project was builed upon a series of libraries for the Python and R programming language.

- [netCDF4](https://unidata.github.io/netcdf4-python/) A Python interface for NetCDF, a set of software libraries and machine-independent data formats that support the creation, access, and sharing of array-oriented scientific data.
- [rpy2](https://rpy2.github.io/doc/v3.5.x/html/index.html): An iterface that allow Python users to work with R language objects.
- [TDA](https://cran.r-project.org/web/packages/TDA/index.html): Is a R language package that provides statistical tools for topological data analysis.
- [NumPy](https://numpy.org/doc/stable/index.html): A package for scientific computing in Python.
- [pandas](https://pandas.pydata.org/docs/index.html): A Python library that provides high-performance, easy-to-use data structures and data analysis tools.
- [scikit-learn](https://scikit-learn.org/stable/index.html): A Python library built on NumPy, SciPy, and matplotlib for data analysis and machine learning.
- [matplotlib](https://matplotlib.org/stable/index.html): A library for creating static, animated, and interactive visualizations in Python.
- [seaborn](https://seaborn.pydata.org/index.html): A data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics for Python programming language.

The details of each Python library are specified in the *requirements.txt* file. 

## Intallation

The user is suggested to install the dependecies indicated in the *requirements.txt* file
in an virtual environment, in order to avoid inconsistencies with the user native enviorment. For that, the following instructions must be followed:

After cloning the repository, create a virtual enviornment in the same folder

```bash
python -m venv name_of_the_venv # The name of the venv is up to the user.
```

Activate the virtual enviorment

```bash
source name_of_the_venv/bin/activate
```

Then install the requirements listed in the requirements.txt using pip.

```bash
pip install -r requirements.txt
```

Finally, the notebook can be executed.

```bash
jupyter notebook
```
## Structure of the project

The structure of the project is the following:

```
|--input/ (Necessary data for the project.)
|
|--src/
|   |--config.py (File and directory names are specified.)
|   |
|   |--extract.py (Extract the information from the netCDF and csv files.)
|   |
|   |--TDA_extractor.R (Performs the sublevel filtration.)
|   |
|   |--transform_and_load.py (Performs the Extract-Load-Transform proces.)
|   |
|   |--plots.py (Plot some graphs.)
|
|--outputs/
|
|--SVM_ECC_ENSO_v3.0.ipynp (A jupyter notebook that apply machine learing over the TDA outputs.)
|
|--requirements.txt (List of libraries used to develop this project and the versions of each one)
|
|--LICENSE.txt (Creative Commons 4.0 License specifications.)
|
|__ README.md (Classified document, those who read it are in danger. Hint: your mother-in-law is involved.)
```  

## Future work

There are some further steps that can be applied in order to improve the resuts of this project like:
- Adding more features as inputs in order to help the classifier get to a linear separation of the data,
- a deeper study of the geometry and topology of the SST fields in order to understand how the three phases of the ENSO are simmilar, apply some transformations surrounding the similarities and check if this new configuration improve performance of the classifier,
- apply another machine learning method like a neural network.

## References

<ol>
    <li>Nobre, G. G. et al. Achieving the reduction of disaster risk by better
predicting impacts of El Niño and La Niña. Progress in Disaster Science,
Volume 2, 2019.</li>
    <li>Diaz, H. F., Markgraf, V. El Nino and the southern oscillation : multiscale
variability and global and regional impacts. Cambridge University Press,
2000.</li>
    <li>Changnon, S. A. El Nino 1997-1998 : the climate event of the century.
Oxford University Press, Inc., 2000.</li>
    <li>Lindsey, R. <a href='https://www.climate.gov/news-features/understanding-climate/climate-
variability-oceanic-ni%C3%B1o-index'>Climate Variability: Oceanic Niño Index</a>. In: Climate |
NOAA[online]. National Oceanic and Atmospheric Administration, 2009
[viewed at: 31 May 2023].</li>
    <li>Edelsbrunner, H. A short course in computational geometry and
topology. Springer, 2014.</li>
    <li>Edelsbrunner, H., Harer, J.. Computational topology : an introduction.
American Mathematical Society, 2010.</li>
    <li>Beltramo, G. et al. Euler characteristic surfaces. Foundations of Data Science, Volume 4, No. 1, 2022.</li>
    <li>Cristianini, N, Shawe-Taylor, J.. Support vector machines and other kernel-based learning methods. Cambridge University Press, 2000.</li>
    <li><a href="https://scikit-learn.org/stable/modules/generated/sklearn.multiclass.OneVsRestClassifier.html#sklearn.multiclass.OneVsRestClassifier">OneVsRestClassifier</a>. In: Scikit-learn: Machine Learning in Python[online] [viewed: 31 May 2023].</li>
</ol>

## Contributing to [ML_TDA-ENSO](https://github.com/Oscar-Amarilla/ML_TDA-ENSO)

Every comment and/or suggestion for improving [ML_TDA-ENSO](https://github.com/Oscar-Amarilla/ML_TDA-ENSO) will be very wellcome, so every user is coordially invated to [open an issue or pull request on GitHub](https://github.com/Oscar-Amarilla/ML_TDA-ENSO/issues).

## License

This work is dedicated to the [public Llicense (CC0 4.0)](https://creativecommons.org/licenses/by/4.0/). See the LICENSE file for all the legalese.
